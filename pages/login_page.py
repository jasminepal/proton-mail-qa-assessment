
import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_label("Email or username")
        self.password = page.get_by_label("Password")
        self.sign_in_button = page.get_by_role(
            "button", name="Sign in"
        )

    def open(self):
        self.page.goto("https://account.proton.me/mail")

    def submit_empty_form(self):
        self.sign_in_button.click()

    def login(self):
        email = os.getenv("PROTON_EMAIL")
        password = os.getenv("PROTON_PASSWORD")

        if not email or not password:
            raise ValueError(
                "Set PROTON_EMAIL and PROTON_PASSWORD in .env"
            )

        self.username.fill(email)
        self.password.fill(password)
        self.sign_in_button.click()

        # Wait until the mailbox loading indicator disappears.
        loading_message = self.page.get_by_text(
            "Loading Proton Mail", exact=False
        )
        expect(loading_message).to_be_hidden(timeout=60000)

        # Confirm the mailbox has rendered.
        expect(
            self.page.get_by_role("button", name="New message")
        ).to_be_visible(timeout=30000)
