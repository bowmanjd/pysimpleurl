"""Test HTTP client."""

import pathlib
import runpy
from urllib.error import URLError
from urllib.parse import urlencode

import pytest

from pysimpleurl import request, run


def test_json_basic_get(httpserver):
    url_path = "/user/1"
    json_sample = {"name": "Sir Robin", "user_id": 1}
    httpserver.expect_request(url_path).respond_with_json(json_sample)
    assert request(httpserver.url_for(url_path)).json() == json_sample


def test_json_get_with_params(httpserver):
    url_path = "/user"
    query_string = "userid=1&movie=Life+of+Brian"
    params = {"userid": 1, "movie": "Life of Brian"}
    json_sample = {"name": "Brian", **params}
    httpserver.expect_request(url_path, query_string=query_string).respond_with_json(
        json_sample
    )
    assert request(httpserver.url_for(url_path), params=params).json() == json_sample


def test_json_get_with_data(httpserver):
    url_path = "/user"
    query_string = "userid=1&movie=Life+of+Brian"
    params = {"userid": 1, "movie": "Life of Brian"}
    json_sample = {"name": "Brian", **params}
    httpserver.expect_request(url_path, query_string=query_string).respond_with_json(
        json_sample
    )
    assert request(httpserver.url_for(url_path), data=params).json() == json_sample


def test_json_post(httpserver):
    url_path = "/user"
    data = {"userid": 100, "year": 1975}
    json_sample = {"name": "Lancelot", "movie": "Holy Grail", **data}
    httpserver.expect_request(url_path, json=data).respond_with_json(json_sample)
    result = request(
        httpserver.url_for(url_path), data=data, method="post", data_as_json=True
    ).json()
    assert result == json_sample


def test_blank_json(httpserver):
    url_path = "/notjson"
    text = "This is not JSON, because it is missing quotes."
    httpserver.expect_request(url_path).respond_with_data(text)
    result = request(httpserver.url_for(url_path)).json()
    assert result == ""


def test_form_encoded_post_with_json_response(httpserver):
    url_path = "/user"
    data = {"userid": 100, "year": 1975}
    json_sample = {"name": "Galahad", "movie": "Holy Grail", **data}
    httpserver.expect_request(
        url_path, method="POST", data=urlencode(data)
    ).respond_with_json(json_sample)
    result = request(
        httpserver.url_for(url_path), data=data, method="post", data_as_json=False
    ).json()
    assert result == json_sample


def test_handle_404(httpserver):
    url_path = "/nonexistent"
    httpserver.expect_request(url_path).respond_with_data("", status=404)
    response = request(httpserver.url_for(url_path))
    assert "not found" in response.body.casefold()
    assert response.status == 404


def test_handle_bad_protocol():
    readme = pathlib.Path.cwd() / "README.md"
    with pytest.raises(URLError):
        request(readme.as_uri())


def test_run(capsys):
    run()
    captured = capsys.readouterr()
    assert "Lorem ipsum dolor sit amet" in captured.out


def test_run_file(capsys):
    runpy.run_module("pysimpleurl", run_name="__main__")
    captured = capsys.readouterr()
    assert "Lorem ipsum dolor sit amet" in captured.out
