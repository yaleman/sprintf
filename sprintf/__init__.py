""" sprintf as a service """

from datetime import datetime, timezone
import json
import logging
import os.path
from pathlib import Path
import re
from typing import  Optional, Union

import click
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from pydantic import BaseModel

IMAGES_BASEDIR = f"{os.path.dirname(__file__)}/images/"
JS_BASEDIR = f"{os.path.dirname(__file__)}/js/"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger instance
logger = logging.getLogger(__name__)

class UserQuery(BaseModel):
    """ Query from a user """
    formatstring: str
    epochtime: Optional[float] = None # Seconds since UNIX epoch

class Result(BaseModel):
    """ Result """
    result: str

class ErrorResult(BaseModel):
    """ error message """
    error: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

match_q = re.compile(r"(?P<matchq>%(?P<num>\d?)[QN]{1})")

class PassableUserQuery(BaseModel):
    """ pass this around """
    formatstring: str
    date_object: datetime

def parse_q_formatstring(query: PassableUserQuery) -> PassableUserQuery:
    """ parses the userquery for a formatstring """
    for found in match_q.finditer(query.formatstring):
        matchdict = found.groupdict()
        # default of 3
        if not matchdict["num"]:
            matchdict["num"] = "3"
        matchdict_num = int(matchdict["num"])
        if query.date_object.microsecond:
            microsecond = str(query.date_object.microsecond).rjust(6,'0')
            microsecond = microsecond[:matchdict_num]
            # if for some reason the system doesn't have
            # that much resolution, zero pad the right hand side.
            microsecond = microsecond.ljust(matchdict_num,"0")
        else:
            microsecond = "0" * matchdict_num
        query.formatstring = query.formatstring.replace(matchdict['matchq'], microsecond)
    return query

def parse_formatstring(query: UserQuery) -> str:
    """ parse the request """

    if query.epochtime is not None:
        date_object = datetime.fromtimestamp(query.epochtime, tz=timezone.utc)
    else:
        date_object = datetime.now(tz=timezone.utc)

    passableobject = PassableUserQuery(
        formatstring=query.formatstring,
        date_object=date_object
    )

    passableobject = parse_q_formatstring(passableobject)
    return passableobject.date_object.strftime(passableobject.formatstring)

@app.post("/parse")
async def parse(query: UserQuery) -> Result:
    """ parse a request then responds """
    result = parse_formatstring(query)

    (json.dumps({
        "formatstring" : query.formatstring,
        "epochtime" : query.epochtime,
        "result": result,
    }))

    return Result( result=result )

@app.get("/js/{filename}", response_model=None)
async def jsfile(filename: str) -> Union[FileResponse, HTMLResponse]:
    """ return a js file """
    filepath = Path(f"{os.path.dirname(__file__)}/js/{filename}").resolve()
    if not filepath.exists() or not filepath.is_file():
        logger.error(f"Can't find {filepath.as_posix()}")
        return HTMLResponse(status_code=404)

    if JS_BASEDIR not in filepath.as_posix():
        logger.warning(json.dumps({
            "action" : "attempt_outside_images_dir",
            "original_path" : filename,
            "resolved_path" : filepath.as_posix()
        }))
        return HTMLResponse(status_code=403)
    return FileResponse(filepath.as_posix())

@app.get("/images/{filename}", response_model=None)
async def images_get(filename: str) -> Union[FileResponse, HTMLResponse]:
    """ return the filename file """
    filepath = Path(f"{os.path.dirname(__file__)}/images/{filename}").resolve()
    if not filepath.resolve().is_file() or not filepath.exists():
        return HTMLResponse(status_code=404)
    if IMAGES_BASEDIR not in filepath.resolve().as_posix():
        logger.warning(json.dumps({
            "action" : "attempt_outside_images_dir",
            "original_path" : filename,
            "resolved_path" : filepath.resolve()
        }))
        return HTMLResponse(status_code=403)
    return FileResponse(filepath.as_posix())

@app.get("/robots.txt", response_model=None)
async def robotstxt() -> HTMLResponse:
    """ robots.txt file """
    return HTMLResponse("""User-agent: *
""")

@app.get("/up", response_model=None)
async def healthcheck() -> HTMLResponse:
    """ healthcheck endpoint """
    return HTMLResponse("OK")

@app.get("/", response_model=None)
async def root() -> HTMLResponse: # pylint: disable=invalid-name
    """ homepage """
    indexfile = Path(f"{os.path.dirname(__file__)}/index.html")
    if not indexfile.exists():
        logger.error("Couldn't find index file!")
        return HTMLResponse(content="File Not Found", status_code=404)
    content = indexfile.read_text(encoding="utf8")

    return HTMLResponse(content)

@click.command()
@click.option("--reload", is_flag=True)
@click.option("--port", type=int, default=8000)
@click.option("--host", type=str, default="0.0.0.0")
@click.option("--proxy-headers", is_flag=True)
def cli(
    reload: bool=False,
    port: int=8000,
    host: str="0.0.0.0",
    proxy_headers: bool=False,
    ) -> None:
    """ sprintf server """
    uvicorn.run(
        app="sprintf:app",
        reload=reload,
        host=host,
        port=port,
        proxy_headers=proxy_headers,
        )
