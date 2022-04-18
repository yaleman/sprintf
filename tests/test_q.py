""" testing for %Q function """

from sprintf import match_q, parse_formatstring, UserQuery

def test_noq() -> None:
    """ tests a string without %Q in it """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d",
            "epochtime": "0",
        }
    )
    assert parse_formatstring(input_data) == "1970-01-01"


def test_bareq() -> None:
    """ test a bare %Q """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d-%Q",
            "epochtime": "0",
        }
    )
    expected_string = "1970-01-01-000"
    assert parse_formatstring(input_data) == expected_string


def test_q4() -> None:
    """ test a  %4Q """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d-%4Q",
            "epochtime": "0.0001",
        }
    )
    expected_string = "1970-01-01-0001"
    assert parse_formatstring(input_data) == expected_string


def test_q6_double() -> None:
    """ test a  %6Q """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d-%6Q-%6Q",
            "epochtime": "0.0001",
        }
    )
    expected_string = "1970-01-01-000100-000100"
    assert parse_formatstring(input_data) == expected_string


def test_q3() -> None:
    """ test a  %3Q """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d-%3Q",
            "epochtime": "0.00001",
        }
    )
    expected_string = "1970-01-01-000"
    assert parse_formatstring(input_data) == expected_string


### test the thing what finds the format string
def test_matchq() -> None:
    """ test some things """
    search_match = match_q.search("%Q")
    assert search_match is not None
    assert search_match.groupdict() == {"num": "", "matchq": "%Q"}


def test_matchq3() -> None:
    """ test %3Q things """
    search_match = match_q.search("%3Q")
    assert search_match is not None
    assert search_match.groupdict() == {"num": "3", "matchq": "%3Q"}
