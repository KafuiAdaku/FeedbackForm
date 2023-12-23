#!/usr/bin/python3
"""Module to create celery task manager for emails"""
from lib.flask_mailplus import send_template_message
from feedback_form.app import create_celery_app
from feedback_form.blueprints.feedback.models import Employee
from feedback_form.blueprints.user.models import User
celery = create_celery_app()


@celery.task()
def deliver_feedback_email(email, message, employee_id, service_rating):
    """
    Send a service review email
    :param email: Email address of the user
    :type email: str
    :param message: Email message
    :type message: str
    :param employee_id: Employee identification
    :type employee_id: int
    :param service_rating: Customer service rating
    :type service_rating: str
    :return: None
    """
    select_employee = Employee.query.get(employee_id)
    if select_employee is None:
        return

    user = User.query.filter_by(email=email).first()
    if user is None:
        return

    ctx = {
            "email": email,
            "message": message,
            "select_employee": select_employee.employee_name,
            "service_rating": service_rating
            }

    send_template_message(subject="[Feedback Form] Customer Service Review",
                          sender=email,
                          recipients=[celery.conf.get("MAIL_USERNAME")],
                          reply_to=email,
                          template="feedback/mail/customer_fdbk_review",
                          ctx=ctx)
    return None


@celery.task()
def deliver_contact_email(name, email, message):
    """
    Send a contact email
    :param name: name of person making inquiry
    :param email: email address of the visitor
    :type email: str
    :param message: Email message
    :type message: str
    :return: None
    """

    ctx = {
            "name": name,
            "email": email,
            "message": message
            }

    send_template_message(subject="[Feedback Form] Inquiry",
                          sender=email,
                          recipients=[celery.conf.get("MAIL_USERNAME")],
                          reply_to=email,
                          template="feedback/mail/inquiry", ctx=ctx)

    return None
