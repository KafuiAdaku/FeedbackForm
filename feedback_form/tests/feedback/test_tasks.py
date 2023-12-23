from feedback_form.extensions import mail
from feedback_form.blueprints.feedback.tasks import (deliver_contact_email,
                                                     deliver_feedback_email)

class TestTasks:
    def test_deliver_feedback_email(self):
        """Deliver feedback email"""
        form = {
                "email": "John Doe",
                "employee_id": 1,
                "service_rating": "Excellent",
                "message": "Excellent service"
                }
        with mail.record_messages() as outbox:
            deliver_feedback_email(form.get("email"),
                                 form.get("message"),
                                 form.get("employee_id"),
                                 form.get("service_rating"))
            assert len(outbox) == 1
            assert form.get("email") in outbox[0].body

    def test_deliver_contact_email(self):
        """Deliver support email"""
        form = {
                "name": "Mary Jane",
                "email": "maryjane@mail.com",
                "message": "Test email for contacting support team"
                }

        with mail.record_messages() as outbox:
            deliver_contact_email(form.get("name"),
                                  form.get("email"),
                                  form.get("message"))

            assert len(outbox) == 1
            assert form.get("name") in outbox[0].body
