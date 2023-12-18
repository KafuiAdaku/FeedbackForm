#!/usr/bin/python3
"""Module for testing view functions on homepage"""
from flask import url_for


class TestPage:
    def test_home_page(self, client):
        """Homepage should respond with status code 200"""
        response = client.get(url_for("page.home"))
        assert response.status_code == 200

    def test_success_page(self, client):
        """Success page should respond with status code 200"""
        response = client.get(url_for("page.success_page"))
        assert response.status_code == 200

    def test_about_us_page(self, client):
        """About us page should respond with status code 200"""
        response = client.get(url_for("page.about_us"))
        assert response.status_code == 200
