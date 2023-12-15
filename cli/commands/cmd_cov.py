#!/usr/bin/python3
"""Module defining cli commands for test coverage report"""
import subprocess
import click


@click.command()
@click.argument("path", default="feedback_form")
def cli(path):
    """
    Runs a test coverage report

    :param path: Test coverage path
    :return: subprocess call result
    """
    cmd = f"py.test --cov-report term-missing --cov {path}"
    return subprocess.call(cmd, shell=True)
