#!/usr/bin/python3
"""Module defining cli commands for running tests"""
import os                                                                                                                                                                       
import subprocess
import click


@click.command()
@click.argument('path', default=os.path.join('feedback_form', 'tests'))
def cli(path):
    """ 
    Run tests with Pytest.
 
    :param path: Test path
    :return: Subprocess call result
    """
    cmd = f"py.test {path}"
    return subprocess.call(cmd, shell=True)
