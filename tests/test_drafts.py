from playwright.sync_api import expect

from pages.compose_page import ComposePage
from pages.mailbox_page import MailboxPage


def test_saved_draft_is_visible(authenticated_page):
    mailbox = MailboxPage(authenticated_page)
    mailbox.open_inbox()
    mailbox.verify_mailbox_loaded()

    compose = ComposePage(authenticated_page)
    compose.open_composer()

    subject = "QA assessment draft verification"
    body = "Verify that Proton Mail saves this draft."

    compose.subject.fill(subject)

    editor = authenticated_page.frame_locator(
        '[data-testid="rooster-iframe"]'
    ).locator('[contenteditable="true"]')
    editor.fill(body)

    # Wait until Proton confirms that the draft has been saved.
    expect(
        authenticated_page.get_by_text("Saved at")
    ).to_be_visible(timeout=15000)

    # Close the composer after saving so it does not mask the Drafts list.
    authenticated_page.get_by_test_id(
        "composer:close-button"
    ).click()

    drafts_link = authenticated_page.get_by_role(
        "link", name="Drafts"
    )
    drafts_link.click()

    draft_subject = authenticated_page.get_by_test_id(
        "message-row:subject"
    ).filter(has_text=subject)

    expect(draft_subject.first).to_be_visible(timeout=15000)