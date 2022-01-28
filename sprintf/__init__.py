""" sprintf as a service """

from datetime import datetime, timezone
import json
import os.path
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel


class UserQuery(BaseModel):
    """ query from a user """
    # datestring: Optional[str] = None
    formatstring: str

app = FastAPI()


def error_result(msg: str):
    """ returns a dict """
    return { "error" : msg }

def parse_user_input(query: UserQuery):
    """ does the handling bit """
    try:
        date_object = datetime.now(tz=timezone.utc)
        return {
            "result" : date_object.strftime(query.formatstring)
        }
    # pylint: disable=broad-except
    except Exception as error:
        return error_result(f"Failed to parse: error {error}")

@app.post("/parse")
async def parse(query: UserQuery):
    """ parse a request then responds """
    print(json.dumps(query, default=str))
    return parse_user_input(query)

@app.get("/chibi.js")
async def chibijs():
    """ return the chibi file """
    return FileResponse(f"{os.path.dirname(__file__)}/chibi-min.js")

@app.get("/favicon.png")
async def favicon():
    """ return the favicon file """
    return FileResponse(f"{os.path.dirname(__file__)}/favicon.png")

@app.get("/")
async def root(f: Optional[str] = None): # pylint: disable=invalid-name
    """ homepage """
    indexfile = Path(f"{os.path.dirname(__file__)}/index.html")
    if not indexfile.exists():
        print("Couldn't find index file!")
        return None
    content = indexfile.read_text(encoding="utf8")

    inputval = "%Y-%m-%d"
    if f is not None:
        if f.strip() != "":
            inputval = f
    content = content.replace("###QUERYSTRING###",inputval)
    return HTMLResponse(content)
