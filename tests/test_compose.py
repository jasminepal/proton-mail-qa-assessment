
import os
from datetime import datetime
from pathlib import Path
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.compose_page import ComposePage


@pytest.mark.skip(reason="Avoid repeated authentication attempts during assessment setup")
def test_inspect_mailbox(page):
    login = LoginPage(page)
    login.open()
    login.login()

    print("\nCurrent URL:", page.url)
    print("Page title:", page.title())

    Path("reports").mkdir(exist_ok=True)
    page.screenshot(
        path="reports/mailbox-debug.png",
        full_page=True,
    )


def test_user_can_open_compose_window(page):
    login = LoginPage(page)
    login.open()
    login.login()

    compose = ComposePage(page)
    compose.open_composer()
    compose.verify_composer_opened()


@pytest.mark.skip(reason="Avoid sending real emails during assessment setup")
def test_user_can_send_email(page):
    recipient = os.getenv("PROTON_EMAIL")
    assert recipient, "Set PROTON_EMAIL in .env"

    login = LoginPage(page)
    login.open()
    login.login()

    compose = ComposePage(page)
    compose.open_composer()
    compose.verify_composer_opened()

    subject = f"QA Automation Test {datetime.now():%Y%m%d%H%M%S}"
    body = "Automated email for the Proton Mail QA assessment."

    compose.fill_email(recipient, subject, body)
    compose.send_email()

    expect(
        page.get_by_text("Message sent", exact=False)
    ).to_be_visible(timeout=15000)
