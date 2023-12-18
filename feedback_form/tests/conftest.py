#!/usr/bin/python3
"""Pytest module"""
import pytest
from feedback_form.app import create_app


@pytest.fixture(scope="session")
def app():
    """
    Setup our flask test app.
    :return: Flask app
    """
    params = {
            "DEBUG": False,
            "TESTING": True
            }

    _app = create_app(settings_override=params)

    # Establish an application contest before running tests
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    """
    Setup an app client. This gets executed for each function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()
