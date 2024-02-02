from typing import List

from click.testing import CliRunner

from ebAlert.main import cli


def get_runner(actions: List[str]):
    runner = CliRunner()
    result = runner.invoke(cli, actions)
    result_list = [part for part in result.output.split("\n") if len(part) > 2]
    return result_list


def test_link_show():
    for test in [['links', '-s'], ['links', '--show']]:
        result_list = get_runner(test)
        assert result_list[0] == ">> List of URL"
        assert result_list[-1] == "<< List of URL"


def test_link_delete():
    for test in [['links', '-r', '123321'], ['links', "--remove_link", '123321']]:
        result_list = get_runner(test)
        assert result_list[0] == ">> Removing link"
        assert result_list[-1] == "<< No link found"


def test_link_clearing():
    for test in [['links', '-c'], ['links', "--clear"]]:
        result_list = get_runner(test)
        assert result_list[0] == ">> Clearing item database"
        assert result_list[-1] == "<< Database cleared"


def test_link_add():
    for test in [["links", "-a", "https://www.kleinanzeigen.de/s-atari/k0"],
                 ['links', '--add_url', "https://www.kleinanzeigen.de/s-atari/k0"]]:
        result_list = get_runner(test)
        assert result_list[0] == ">> Adding url"
        assert result_list[-1][0:2] == "<<"


def test_link_initialized():
    for test in [["links", "-i"], ["links", "--init"]]:
        result_list = get_runner(test)
        assert result_list[0] == ">> Initializing database"
        assert result_list[-1] == "<< Database initialized"


def test_start():
    result_list = get_runner(["start"])
    assert result_list[0] == ">> Starting Ebay alert"
    assert result_list[-1] == "<< Ebay alert finished"


if __name__ == "__main__":
    pass
