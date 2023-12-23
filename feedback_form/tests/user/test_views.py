from flask import url_for
from lib.tests import assert_status_with_message, ViewTestMixin
from feedback_form.blueprints.user.models import User


class TestLogin(ViewTestMixin):
    def test_login_page(self):
        """Login page should respond with a success 200."""
        response = self.client.get(url_for("user.login"))
        assert response.status_code == 200
    
    def test_login(self):
        """Login should redirect with a message."""
        response = self.login()
        assert response.status_code == 200
    
    def test_login_activity(self):
        """Login successfully and update login stats."""
        user = User.find_by_identity("admin@local.host")
        old_sign_in_count = user.sign_in_count

        response = self.login()
        new_sign_in_count = user.sign_in_count

        assert response.status_code == 200
        assert (old_sign_in_count + 1) == new_sign_in_count

    def test_login_disabled(self):
        """Login should redirect with a message."""
        response = self.login(identity='disabled@local.host')

        assert_status_with_message(200, response,
                                   "This account has been disabled.")
    
    def test_login_fail(self):
        """Login failure due to invalid credentials."""
        response = self.login(identity="foobar@mail.com")
        assert_status_with_message(200, response, "Identity or password is incorrect.")

    def test_logout(self):
        """Logout successfully."""
        self.login()
        response = self.logout()
        assert_status_with_message(200, response, "You have been logged out.")
    


