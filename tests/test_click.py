""" testing click functionality """

from click.testing import CliRunner
from sprintf import cli

def test_command_help() -> None:
    """ test that something works using click """
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    print(result)
