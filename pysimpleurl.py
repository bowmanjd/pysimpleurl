#!/usr/bin/env python3

"""List and process image tags for a repository in a Docker v2 registry."""


import json
import typing
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message


class Response(typing.NamedTuple):
    """Container for HTTP response."""

    body: str
    headers: Message
    status: int
    error_count: int = 0

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
    jsonformat: bool = True,
    error_count: int = 0,
) -> Response:
    """
    Perform HTTP request.

    Args:
        url: url to fetch
        data: dict of keys/values to be encoded and submitted
        params: dict of keys/values to be encoded in URL query string
        headers: optional dict of request headers
        method: HTTP method , such as GET or POST
        jsonformat: if True, data will be JSON-encoded
        error_count: optional current count of HTTP errors, to manage recursion

    Returns:
        A dict with headers, body, status code, and, if applicable, object
        rendered from JSON
    """
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"User-Agent": "pysimpleurl", "Accept": "*/*", **headers}

    if method == "GET":
        params = {**params, **data}
        data = None

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        if jsonformat:
            request_data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = urllib.parse.urlencode(data).encode()

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers, method=method
    )

    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = Response(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                ),
            )
    except urllib.error.HTTPError as e:
        response = Response(
            body="", headers=e.headers, status=e.code, error_count=error_count + 1
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
