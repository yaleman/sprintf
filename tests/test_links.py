""" fastapi / requests-html tests that check that all the links/references on the page work... """


from typing import List

from fastapi.testclient import TestClient
import pytest
import requests
import requests.exceptions

from requests_html import HTML, Element # type: ignore

from sprintf import app

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@pytest.fixture(name="client")
def fixture_client() -> TestClient:
    """ client factory """

    return TestClient(app)


async def test_links(client: TestClient) -> None:
    """ testing """
    # asession = AsyncHTMLSession()
    # r = await asession.get('https://stackoverflow.org/')
    result = client.get("/" )

    parsed = HTML(html=result.content)

    tags_to_find = {
        "a": "href",
        "link": "href",
        "meta": "content",
        "script": "src",
        "img": "src",
    }

    links_to_check: List[str] = []

    for tag in tags_to_find:  # pylint: disable=consider-using-dict-items
        elements: List[Element] = parsed.find(tag)
        for element in elements:
            if tags_to_find[tag] in element.attrs:
                value: str = element.attrs[tags_to_find[tag]]
                if value.lower().startswith("htt") or value.startswith("/"):
                    print(f"Adding {value} to checks.")
                    links_to_check.append(value)

    failed_links: List[str] = []

    for link in links_to_check:
        try:
            if link.startswith("http") and "sprintf.yaleman.org" not in link:
                print(f"Web: {link}")
                testresult = requests.get(link, timeout=5)
            else:
                print(f"Local: {link}")
                testresult = client.get(link) #type: ignore
            testresult.raise_for_status()
            assert testresult
            print(f"OK: {link} ")
        except requests.exceptions.HTTPError as httperror:
            if testresult.status_code == 404:
                failed_links.append(link)
            else:
                pytest.fail(str(httperror))
    if failed_links:
        pytest.fail("\n".join([f"404 pulling {link}" for link in failed_links]))
