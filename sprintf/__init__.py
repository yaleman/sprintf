""" sprintf as a service """

from datetime import datetime, timezone
import json
import os.path
from pathlib import Path
from typing import Dict, Optional, Union

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

DEFAULT_FORMATSTRING = "%Y-%m-%d"
IMAGES_BASEDIR = f"{os.path.dirname(__file__)}/images/"
JS_BASEDIR = f"{os.path.dirname(__file__)}/js/"

class UserQuery(BaseModel):
    """ query from a user """
    # datestring: Optional[str] = None
    action: str = "parse"
    formatstring: str

class ErrorResult(BaseModel):
    """ error message """
    error: str


app = FastAPI()

@app.post("/parse")
async def parse(query: UserQuery) -> Dict[str, str]:
    """ parse a request then responds """
    try:
        date_object = datetime.now(tz=timezone.utc)
        return {
            "result" : date_object.strftime(query.formatstring)
        }
    # pylint: disable=broad-except
    except Exception as error:
        return ErrorResult(error=f"Failed to parse: error {error}").dict()

@app.get("/js/{filename}")
async def jsfile(filename: str) -> Union[FileResponse, HTMLResponse]:
    """ return a js file """
    filepath = Path(f"{os.path.dirname(__file__)}/js/{filename}").resolve()
    if not filepath.exists() or not filepath.is_file():
        print(f"Can't find {filepath.as_posix()}")
        return HTMLResponse(status_code=404)

    if not JS_BASEDIR in filepath.as_posix():
        print(json.dumps({
            "action" : "attempt_outside_images_dir",
            "original_path" : filename,
            "resolved_path" : filepath.as_posix()
        }))
        return HTMLResponse(status_code=403)
    return FileResponse(filepath.as_posix())


@app.head("/images/{filename}")
async def images_head(filename: str) -> Union[FileResponse, HTMLResponse]:
    """ return the filename file """
    filepath = Path(f"{os.path.dirname(__file__)}/images/{filename}").resolve()

    if not filepath.exists() or not filepath.is_file():
        return HTMLResponse(status_code=404)
    if not IMAGES_BASEDIR in filepath.as_posix():
        print(json.dumps({
            "action" : "attempt_outside_images_dir",
            "original_path" : filename,
            "resolved_path" : filepath.as_posix()
        }))
        return HTMLResponse(status_code=403)

    return HTMLResponse(
        status_code=200,
        headers={
            "Content-Length" : str(filepath.stat().st_size),
            }
        )

@app.get("/images/{filename}")
async def images_get(filename: str) -> Union[FileResponse, HTMLResponse]:
    """ return the filename file """
    filepath = Path(f"{os.path.dirname(__file__)}/images/{filename}").resolve()
    if not filepath.resolve().is_file() or not filepath.exists():
        return HTMLResponse(status_code=404)
    if not IMAGES_BASEDIR in filepath.resolve().as_posix():
        print(json.dumps({
            "action" : "attempt_outside_images_dir",
            "original_path" : filename,
            "resolved_path" : filepath.resolve()
        }))
        return HTMLResponse(status_code=403)
    return FileResponse(filepath.as_posix())

@app.get("/robots.txt")
async def robotstxt() -> HTMLResponse:
    """ robots.txt file """
    return HTMLResponse("""User-agent: *
""")

@app.get("/up")
async def healthcheck() -> HTMLResponse:
    """ healthcheck endpoint """
    return HTMLResponse("OK")

@app.get("/")
async def root(f: Optional[str] = None) -> HTMLResponse: # pylint: disable=invalid-name
    """ homepage """
    indexfile = Path(f"{os.path.dirname(__file__)}/index.html")
    if not indexfile.exists():
        print("Couldn't find index file!")
        return HTMLResponse(content="File Not Found", status_code=404)
    content = indexfile.read_text(encoding="utf8")

    inputval = "%Y-%m-%d"
    if f is not None and f.strip() != "":
        inputval = f.strip()
    content = content.replace("###QUERYSTRING###",inputval)
    return HTMLResponse(content)
