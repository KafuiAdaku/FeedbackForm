from feedback_form.extensions import mail
from feedback_form.blueprints.user.tasks import deliver_password_reset_email
from feedback_form.blueprints.user.models import User


class TestTasks:
    def test_deliver_password_reset_email(self, token):
        """
        Test that the password reset email is sent.
        """
        with mail.record_messages() as outbox:
            user = User.find_by_identity('admin@local.host')
            deliver_password_reset_email(user.id, token)

            assert len(outbox) == 1
            assert token.decode() in outbox[0].body
