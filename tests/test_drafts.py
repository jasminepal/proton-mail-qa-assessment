from playwright.sync_api import expect
from datetime import datetime
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
    


def test_draft_content_persists_after_reopening(authenticated_page):
    from datetime import datetime

    page = authenticated_page
    page.goto("https://mail.proton.me/u/1/inbox")

    subject = f"QA Draft {datetime.now().strftime('%Y%m%d%H%M%S')}"
    body = "This is a test email body for draft persistence verification."

    page.get_by_role("button", name="New message").first.click()

    composer = page.get_by_role("region", name="Composer: New message")
    expect(composer).to_be_visible(timeout=15000)

    page.get_by_role("textbox", name="Subject").fill(subject)

    # Access the editable body inside the iframe.
    body_editor = page.frame_locator(
        '[data-testid="rooster-iframe"]'
    ).locator('[contenteditable="true"]')

    expect(body_editor).to_be_visible(timeout=15000)
    body_editor.fill(body)

    # Wait for the draft to save.
    expect(page.get_by_text("Saved at")).to_be_visible(timeout=15000)
    page.get_by_test_id("composer:close-button").click()

    # Open Drafts and reopen the specific draft.
    page.get_by_text("Drafts", exact=True).first.click()

    draft = page.get_by_test_id("message-row:subject").filter(
        has_text=subject
    )
    expect(draft).to_be_visible(timeout=15000)
    draft.click()

    # Verify that both subject and body were retained.
    expect(page.get_by_role("textbox", name="Subject")).to_have_value(subject)

    reopened_body = page.frame_locator(
        '[data-testid="rooster-iframe"]'
    ).locator('[contenteditable="true"]')

    expect(reopened_body).to_be_visible(timeout=15000)
    expect(reopened_body).to_contain_text(body)



def test_draft_subject_persists_after_reopening(authenticated_page):
    page = authenticated_page
    page.goto("https://mail.proton.me/u/1/inbox")

    subject = f"QA Persistence {datetime.now().strftime('%Y%m%d%H%M%S')}"

    page.get_by_role("button", name="New message").first.click()

    composer = page.get_by_role("region", name="Composer: New message")
    expect(composer).to_be_visible(timeout=15000)

    page.get_by_role("textbox", name="Subject").fill(subject)

    expect(page.get_by_text("Saved at")).to_be_visible(timeout=15000)

    page.get_by_test_id("composer:close-button").click()

    page.get_by_text("Drafts", exact=True).first.click()

    draft = page.get_by_test_id("message-row:subject").filter(
        has_text=subject
    )
    expect(draft).to_be_visible(timeout=15000)
    draft.click()

    expect(
        page.get_by_role("textbox", name="Subject")
    ).to_have_value(subject)
