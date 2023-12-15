#!/usr/bin/python3
"""Module for implemeting click commands for database"""
import click

from sqlalchemy_utils import database_exists, create_database

from feedback_form.app import create_app
from feedback_form.extensions import db
from feedback_form.blueprints.user.models import User

# Create an app context for the database connection
app = create_app()
db.app = app

@click.group()
def cli():
    """
    Run postgresql related task
    """
    pass


@click.command()
@click.option("--with-testdb/--no-with-testdb", default=False,
              help="Create a test db too")
def init(with_testdb):
    """
    Initialize the databse

    :param with_testdb: Create a test database
    :return: None
    """
    from sqlalchemy.exc import OperationalError

    with app.app_context():
        try:
            db.drop_all()
            db.create_all()

            if with_testdb:
                db_uri = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"

                if not database_exists(db_uri):
                    create_database(db_uri)

        except OperationalError as e:
            print(f"Error: {e}")
            print("Failed to initialize the database. Make sure it exists \
and the connection parameters are correct.")

    return None


@click.command()
def seed():
    """
    Seed the database with an initial user

    :return: User instance
    """
    with app.app_context():
        if User.find_by_identity(app.config["SEED_ADMIN_EMAIL"]) is not None:
            return None

    params = {
            "role": "admin",
            "email": app.config["SEED_ADMIN_EMAIL"],
            "password": app.config["SEED_ADMIN_PASSWORD"]
            }
    return User(**params).save()


@click.command()
@click.option("--with-testdb/--no-with-testdb", default=False,
              help="Create a test db too?")
@click.pass_context
def reset(ctx, with_testdb):
    """
    Initialize data base and seed automatically

    :param with_testdb: Create a test database
    :return: None
    """
    with app.app_context():
        ctx.invoke(init, with_testdb=with_testdb)
        ctx.invoke(seed)

    return None


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
