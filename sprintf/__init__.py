""" sprintf as a service """

from datetime import datetime, timezone
import json
import os.path
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel


DEFAULT_FORMATSTRING = "%Y-%m-%d"

class UserQuery(BaseModel):
    """ query from a user """
    # datestring: Optional[str] = None
    action: str = "parse"
    formatstring: str

class ErrorResult(BaseModel):
    """ error message """
    error: str


app = FastAPI()

def parse_user_input(query: UserQuery) -> Dict[str, str]:
    """ does the handling bit """
    try:
        date_object = datetime.now(tz=timezone.utc)
        return {
            "result" : date_object.strftime(query.formatstring)
        }
    # pylint: disable=broad-except
    except Exception as error:
        return ErrorResult(error=f"Failed to parse: error {error}").dict()

@app.post("/parse")
async def parse(query: UserQuery) -> Dict[str, str]:
    """ parse a request then responds """
    print(json.dumps(query, default=str))
    return parse_user_input(query)

@app.get("/chibi.js")
async def chibijs() -> FileResponse:
    """ return the chibi file """
    return FileResponse(f"{os.path.dirname(__file__)}/chibi-min.js")

@app.get("/favicon.png")
async def favicon() -> FileResponse:
    """ return the favicon file """
    return FileResponse(f"{os.path.dirname(__file__)}/favicon.png")

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
