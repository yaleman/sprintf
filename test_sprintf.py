""" test module for sprintf """
from datetime import datetime, timezone

from pathlib import Path

from fastapi.testclient import TestClient
import pytest
from sprintf import app, DEFAULT_FORMATSTRING

client = TestClient(app)


def test_read_main():
    """ test the healthcheck works """
    response = client.get("/up")
    assert response.status_code == 200
    assert response.text == "OK"

def test_index_html():
    """ gets the index.html"""
    indexhtml = Path("./sprintf/index.html")

    if not indexhtml.exists():
        pytest.fail("Couldn't find index.html on the filesystem, can't test for it in the API")
    expected_result = indexhtml.read_text(encoding="utf8").replace(
        "###QUERYSTRING###", DEFAULT_FORMATSTRING)
    response = client.get("/")
    assert response.text == expected_result

def test_parse():
    """ gets a date """

    expected_result = datetime.now(tz=timezone.utc).strftime("%Y-%m")
    response = client.post(url="/parse", json = { "formatstring" : "%Y-%m" })
    assert response.json() == { "result" : expected_result }
