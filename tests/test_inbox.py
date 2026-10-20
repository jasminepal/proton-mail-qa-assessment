from playwright.sync_api import expect
from pages.mailbox_page import MailboxPage


def test_mailbox_is_accessible(authenticated_page):
    mailbox = MailboxPage(authenticated_page)

    mailbox.open_inbox()
    mailbox.verify_mailbox_loaded()