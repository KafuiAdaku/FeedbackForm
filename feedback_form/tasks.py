from celery import Celery
from flask_mail import Message
from flask import current_app
from feedback_form.app import create_celery_app
from feedback_form.extentions import mail

celery = create_celery_app()

@celery.task
def send_async_email(emp_fb, service_fb, comments):
    with current_app.app_context():
        sender = current_app.config['MAIL_USERNAME']
        subject = 'New Feedback Submission'
        body = f"Employee Feedback: {emp_fb}\nService Rating: {service_fb}\nAdditional Comment: {comments}"

        admin_email = current_app.config['ADMIN_EMAIL']

        msg = Message(subject, sender=sender, recipients=[admin_email], body=body)
        mail.send(msg)

