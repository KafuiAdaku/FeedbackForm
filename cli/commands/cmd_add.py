import click
import random

from datetime import datetime, timezone

from faker import Faker

from feedback_form.app import create_app
from feedback_form.extensions import db
from feedback_form.blueprints.user.models import User
from feedback_form.blueprints.feedback.models import Employee, Review

# Create an app context for the database connection.
app = create_app()
db.app = app

fake = Faker()


def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo(f'Created {count} {model_label}')

    return None


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is much more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :return: None
    """
    with app.app_context():
        if model == Employee:
            Review.query.filter(Review.employee_id.in_(
                                db.session.query(Employee.id)
                                )).delete(synchronize_session='fetch')
            db.session.commit()

        model.query.delete()
        db.session.commit()
        db.session.bulk_insert_mappings(model, data)
        db.session.commit()

        _log_status(model.query.count(), label)

    return None


@click.group()
def cli():
    """ Add items to the database. """
    pass


@click.command()
def users():
    """
    Generate fake users.
    """
    random_emails = []
    data = []

    click.echo('Working...')

    # Ensure we get about 100 unique random emails.
    for i in range(0, 99):
        random_emails.append(fake.email())

    admin_email = app.config["SEED_ADMIN_EMAIL"]
    random_emails.append(app.config['SEED_ADMIN_EMAIL'])
    random_emails = list(set(random_emails))

    while True:
        if not random_emails:
            break

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        created_on = datetime.utcfromtimestamp(
            float(fake_datetime)).replace(tzinfo=timezone.utc)

        random_percent = random.random()

        if random_percent >= 0.05:
            role = 'member'
        else:
            role = 'admin'

        email = random_emails.pop()

        random_percent = random.random()

        if random_percent >= 0.5:
            random_trail = str(int(round((random.random() * 1000))))
            username = fake.first_name() + random_trail
        else:
            username = None

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        current_sign_in_on = datetime.utcfromtimestamp(
            float(fake_datetime)).replace(tzinfo=timezone.utc)

        params = {
            'created_on': created_on,
            'updated_on': created_on,
            'role': role,
            'email': email,
            'username': username,
            'password': User.encrypt_password('password'),
            'sign_in_count': random.random() * 100,
            'current_sign_in_on': current_sign_in_on.replace(tzinfo=timezone.utc),
            'current_sign_in_ip': fake.ipv4(),
            'last_sign_in_on': current_sign_in_on,
            'last_sign_in_ip': fake.ipv4()
        }

        # Ensure the seeded admin is always an admin with the seeded password.
        if email == app.config['SEED_ADMIN_EMAIL']:
            password = User.encrypt_password(app.config['SEED_ADMIN_PASSWORD'])

            params['role'] = 'admin'
            params['password'] = password

        data.append(params)

    return _bulk_insert(User, data, 'users')


@click.command()
def employees():
    """
    Generate fake employees
    """
    random_names = []
    data = []

    click.echo("Working ...")

    for _ in range(0, 10):
        random_names.append(fake.name())

    random_names = list(set(random_names))

    while True:
        if not random_names:
            break

        name = random_names.pop()
        params = {
                "employee_name": name
                }
        data.append(params)

    return _bulk_insert(Employee, data, "employees")


@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(users)
    ctx.invoke(employees)

    return None


cli.add_command(users)
cli.add_command(employees)
cli.add_command(all)
