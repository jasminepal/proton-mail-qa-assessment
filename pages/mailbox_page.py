from playwright.sync_api import Page, expect


class MailboxPage:
    def __init__(self, page: Page):
        self.page = page
        self.new_message_button = page.get_by_role(
            "button", name="New message"
        )

    def open_inbox(self):
        self.page.goto("https://mail.proton.me/u/1/inbox")

    def verify_mailbox_loaded(self):
        expect(self.new_message_button.first).to_be_visible(
            timeout=15000
        )

    def open_compose(self):
        self.new_message_button.first.click()