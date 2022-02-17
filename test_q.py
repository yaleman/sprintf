""" testing for %Q function """

from sprintf import match_q, parse_formatstring, UserQuery


def test_noq():
    """ tests a string without %Q in it """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d",
            "epochtime": "0",
        }
    )
    assert parse_formatstring(input_data) == "1970-01-01"


def test_bareq():
    """ test a bare %Q """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d-%Q",
            "epochtime": "0",
        }
    )
    expected_string = "1970-01-01-000"
    assert parse_formatstring(input_data) == expected_string


def test_q4():
    """ test a  %4Q """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d-%4Q",
            "epochtime": "0.0001",
        }
    )
    expected_string = "1970-01-01-0001"
    assert parse_formatstring(input_data) == expected_string


def test_q4_double():
    """ test a  %4Q """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d-%4Q-%4Q",
            "epochtime": "0.0001",
        }
    )
    expected_string = "1970-01-01-0001-0001"
    assert parse_formatstring(input_data) == expected_string


def test_q2():
    """ test a  %2Q """
    input_data = UserQuery.parse_obj(
        {
            "formatstring": "%Y-%m-%d-%2Q",
            "epochtime": "0.00001",
        }
    )
    expected_string = "1970-01-01-00"
    assert parse_formatstring(input_data) == expected_string


### test the thing what finds the format string
def test_matchq():
    """ test some things """
    assert match_q.search("%Q").groupdict() == {"num": "", "matchq": "%Q"}


def test_matchq3():
    """ test %3Q things """
    assert match_q.search("%3Q").groupdict() == {"num": "3", "matchq": "%3Q"}
