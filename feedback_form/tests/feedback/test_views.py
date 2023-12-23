from flask import url_for
from lib.tests import assert_status_with_message

class TestFeedback:
    def test_feedback_page(self, client):
        """Feedback page should respond with a 302 if a user is not logged in."""
        response = client.get(url_for("feedback.index"))
        assert response.status_code == 302

    def test_contact_page(self, client):
        """Contact page should responde with a success of 200"""
        response = client.get(url_for("feedback.contact"))
        assert response.status_code == 200

    def test_feedback_form(self, client):
        """Feedback form should redirect with a message."""
        form = {
                "employee_feedback": "John Doe",
                "service_feedback": "Excellent",
                "additional_comments": "Some random comment",
                }
        response = client.post(url_for("feedback.index"), data=form,
                               follow_redirects=True)
        assert_status_with_message(400, response, "Bad Request")

    def test_contact_form(self, client):
        """Contact form should redirects with a message."""
        form = {
                "name": "Mary Jane",
                "email": "foobar@mail.com",
                "message": "Another random message"
                }
        response = client.post(url_for("feedback.contact"), data=form,
                              follow_redirects=True)
        assert_status_with_message(200, response, "Your message")

