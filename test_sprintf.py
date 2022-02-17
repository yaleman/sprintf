""" test module for sprintf """
from datetime import datetime, timezone

# import re

from pathlib import Path

from fastapi.testclient import TestClient
import pytest
from sprintf import app

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
        pytest.fail(
            "Couldn't find index.html on the filesystem, can't test for it in the API"
        )
    expected_result = indexhtml.read_text(encoding="utf8")
    response = client.get("/")
    assert response.text == expected_result


def test_parse():
    """ gets a date """

    expected_result = datetime.now(tz=timezone.utc).strftime("%Y-%m")
    response = client.post(url="/parse", json={"formatstring": "%Y-%m"})
    assert response.json() == {"result": expected_result}


def test_input_epochtime():
    """ tests that inputs work """

    response = client.post(
        url="/parse",
        json={
            "formatstring": "%Y-%m-%d %H:%m:%S",
            "epochtime": "0",
        },
    )

    assert response.json() == {"result": "1970-01-01 00:01:00"}

    response = client.post(
        url="/parse",
        json={
            "formatstring": "%Y-%m-%d %H:%m:%S",
            "epochtime": "10",
        },
    )

    assert response.json() == {"result": "1970-01-01 00:01:10"}


# TODO: finish this for #2
# # def test_parse_n():
#     """ tests the %N functionality """


#     epochtime = 0.0001

#     # regex_match = re.compile("")
#     expected_result = "1970-01-01 10:00:00.0001"
#     response = client.post(url="/parse", json = {
#         "formatstring" : "%Y-%m-%d %H:%m:%S.%N" ,
#         "epochtime" : epochtime
#     })

#     assert response.json() == { "result" : expected_result }


def test_parse_q_live():
    """ tests the %Q functionality, actually running through fastAPI """
    epochtime = 0.001
    expected_result = "1970-01-01 00:00:00.001"
    response = client.post(
        url="/parse",
        json={"formatstring": "%Y-%m-%d %H:%M:%S.%Q", "epochtime": epochtime},
    )

    assert response.json() == {"result": expected_result}
