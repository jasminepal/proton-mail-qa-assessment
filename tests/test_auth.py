
from playwright.sync_api import expect
from pages.login_page import LoginPage
import pytest


def test_sign_in_page_loads(page):
    login = LoginPage(page)
    login.open()

    expect(
        page.get_by_role("heading", name="Sign in")
    ).to_be_visible()

    expect(login.username).to_be_visible()
    expect(login.password).to_be_visible()
    expect(login.sign_in_button).to_be_visible()


def test_sign_in_with_empty_fields(page):
    login = LoginPage(page)
    login.open()
    login.submit_empty_form()

    expect(
        page.get_by_role("heading", name="Sign in")
    ).to_be_visible()


@pytest.mark.skip(
    reason="Temporarily disabled to avoid repeated authentication attempts"
)
def test_valid_login_reaches_mailbox(page):
    login = LoginPage(page)
    login.open()
    login.login()

    # Wait for the mailbox's Inbox navigation item.
    inbox = page.get_by_text("Inbox", exact=True).first
    expect(inbox).to_be_visible(timeout=45000)
