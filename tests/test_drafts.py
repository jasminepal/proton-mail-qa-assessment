import pytest
from pages.mailbox_page import MailboxPage
from pages.drafts_page import DraftsPage


@pytest.mark.skip(
    reason="Requires verified draft-saving flow and authenticated test session"
)
def test_saved_draft_is_visible(authenticated_page):
    mailbox = MailboxPage(authenticated_page)
    mailbox.open_inbox()

    drafts = DraftsPage(authenticated_page)
    drafts.verify_draft_saved()