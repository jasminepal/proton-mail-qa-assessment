
import pytest
from playwright.sync_api import expect
from pages.compose_page import ComposePage
from pages.mailbox_page import MailboxPage


def test_user_can_open_compose_window(authenticated_page):
    mailbox = MailboxPage(authenticated_page)
    mailbox.open_inbox()
    mailbox.verify_mailbox_loaded()

    compose = ComposePage(authenticated_page)
    compose.open_composer()
    compose.verify_composer_opened()


def test_user_can_enter_message_fields(authenticated_page):
    mailbox = MailboxPage(authenticated_page)
    mailbox.open_inbox()
    mailbox.verify_mailbox_loaded()

    compose = ComposePage(authenticated_page)
    compose.open_composer()

    compose.recipient.fill("assessment-test@example.com")
    compose.subject.fill("QA assessment draft")

    # Locate the rich-text editor inside the iframe.
    editor = authenticated_page.frame_locator(
        '[data-testid="rooster-iframe"]'
    ).locator('[contenteditable="true"]')

    expect(editor).to_be_visible(timeout=15000)

    message = "This is a draft created for QA assessment testing."
    editor.fill(message)

    expect(compose.subject).to_have_value("QA assessment draft")
    expect(editor).to_contain_text(message)


# @pytest.mark.skip(
#     reason="Sending requires a controlled recipient and verified send confirmation"
# )
# def test_user_can_send_email(authenticated_page):
#     # Implement only when a controlled test recipient is configured
#     # and the send confirmation locator is verified.
#     pass


def test_send_without_recipient_shows_validation(authenticated_page):
    mailbox = MailboxPage(authenticated_page)
    mailbox.open_inbox()
    mailbox.verify_mailbox_loaded()

    compose = ComposePage(authenticated_page)
    compose.open_composer()

    compose.subject.fill("QA validation test")

    send_button = authenticated_page.get_by_role(
        "button", name="Send"
    )
    send_button.click()

    # A message without a recipient should not be sent.
    expect(
        authenticated_page.get_by_role("region").filter(
            has=authenticated_page.get_by_role(
                "textbox", name="Subject"
            )
        )
    ).to_be_visible()
