from django.contrib.auth.models import User
from integration_tests.testing_tools import SeleniumTestCase
import time

class AuthenticationFormTest(SeleniumTestCase):
    def test_authentication_form(self):
        # Create a user to login with
        user = User.objects.create_user(
            username="test@user.com", email="test@user.com", password="12345"
        )

        # Go to the login page
        self.driver.get(self.live_server_url + "/login/")

        # Find HTML elements
        email_input = self.driver.find_element_by_id("email")
        password_input = self.driver.find_element_by_id("password")
        error_message = self.driver.find_element_by_css_selector(".error")
        login_button = self.driver.find_element_by_id("btn-login")

        # Type in an email that doesn't exist
        email_input.send_keys("wrong@user.com")

        # Ensure that the submit button is disabled
        self.assertFalse(login_button.is_enabled())

        # Type in a password
        password_input.send_keys("wrongpassword")
        login_button.click()

        # Wait for request
        time.sleep(0.5)

        # Check that the error message is displayed
        self.assertEqual(error_message.text, "A user with this email address does not exist.")

        # Type in an email that does exist but with the wrong password
        email_input.clear()
        email_input.send_keys(user.email)
        login_button.click()

        # Wait for request
        time.sleep(0.5)

        # Check that the correct error message is displayed
        self.assertEqual(error_message.text, "You entered the wrong password.")

        # Type in the correct email and password
        password_input.clear()
        password_input.send_keys("12345")
        login_button.click()

        # Wait for request
        time.sleep(0.5)

        # Check that the user is logged in
        self.assertEqual(self.driver.current_url, self.live_server_url + "/home/")
