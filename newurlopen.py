#!/usr/bin/env python3

"""Basic example of an HTTP client that does not depend on any external libraries."""


import json
import typing
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message


class SafeOpener(urllib.request.OpenerDirector):
    """An opener with configurable set of handlers."""

    def __init__(self, handlers: typing.Iterable = None):
        """
        Instantiate an OpenDirector with selected handlers.

        Args:
            handlers: an Iterable of handler classes
        """
        super().__init__()
        handlers = handlers or (
            urllib.request.ProxyHandler,
            urllib.request.UnknownHandler,
            urllib.request.HTTPHandler,
            urllib.request.HTTPDefaultErrorHandler,
            urllib.request.HTTPRedirectHandler,
            urllib.request.HTTPSHandler,
            urllib.request.HTTPErrorProcessor,
        )

        for handler in handlers:
            self.add_handler(handler())


urllib.request.install_opener(SafeOpener())


class Response(typing.NamedTuple):
    """Container for HTTP response."""

    body: str
    headers: Message
    status: int
    url: str

    def json(self) -> typing.Any:
        """
        Decode body's JSON.

        Returns:
            Pythonic representation of the JSON object
        """
        try:
            output = json.loads(self.body)
        except json.JSONDecodeError:
            output = ""
        return output


def request(
    url: str,
    data: dict = None,
    params: dict = None,
    headers: dict = None,
    method: str = "GET",
    data_as_json: bool = True,
) -> Response:
    """
    Perform HTTP request.

    Args:
        url: url to fetch
        data: dict of keys/values to be encoded and submitted
        params: dict of keys/values to be encoded in URL query string
        headers: optional dict of request headers
        method: HTTP method , such as GET or POST
        data_as_json: if True, data will be JSON-encoded

    Returns:
        A dict with headers, body, status code, and, if applicable, object
        rendered from JSON
    """
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"Accept": "application/json", **headers}

    if method == "GET":
        params = {**params, **data}
        data = None

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        if data_as_json:
            request_data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = urllib.parse.urlencode(data).encode()

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers, method=method
    )

    with urllib.request.urlopen(httprequest) as httpresponse:
        response = Response(
            headers=httpresponse.headers,
            status=httpresponse.status,
            body=httpresponse.read().decode(
                httpresponse.headers.get_content_charset("utf-8")
            ),
            url=httpresponse.url,
        )

    return response


def run() -> None:
    """Run as script."""
    url = "https://jsonplaceholder.typicode.com/posts"
    data = {
        "title": "Sample post 1",
        "body": "Lorem ipsum dolor sit amet",
        "userId": 22,
    }
    response = request(url, data=data, method="post")
    json_response = response.json()
    print(json.dumps(json_response, indent=2))


if __name__ == "__main__":
    run()
