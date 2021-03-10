"""Helpers useful for any tests."""

import ssl

import pytest
import trustme  # type: ignore


@pytest.fixture(scope="session")
def httpserver_ssl_context():
    """Set SSL context.

    Returns:
        SSL context
    """
    ca = trustme.CA()
    client_context = ssl.SSLContext()
    server_context = ssl.SSLContext()
    server_cert = ca.issue_cert("test-host.example.org")
    ca.configure_trust(client_context)
    server_cert.configure_cert(server_context)

    def default_context():
        return client_context

    ssl._create_default_https_context = default_context

    return server_context
