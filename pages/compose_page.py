
from playwright.sync_api import Page, expect


class ComposePage:
    def __init__(self, page: Page):
        self.page = page
        self.composer = page.get_by_role(
            "region", name="Composer: New message"
        )
        self.recipient = self.composer.get_by_role(
            "textbox", name="To"
        )
        self.subject = self.composer.get_by_role(
            "textbox", name="Subject"
        )
        self.send_button = self.composer.get_by_role(
            "button", name="Send", exact=True
        )

    def open_composer(self):
        self.page.get_by_role(
            "button", name="New message"
        ).first.click()
        expect(self.composer).to_be_visible(timeout=15000)

    def verify_composer_opened(self):
        expect(self.composer).to_be_visible()
        expect(self.recipient).to_be_visible()
        expect(self.subject).to_be_visible()
        expect(self.send_button).to_be_visible()

    def fill_email(self, recipient, subject, body):
        self.recipient.fill(recipient)
        self.recipient.press("Enter")
        self.subject.fill(subject)

        # Proton's message editor may be inside an iframe.
        # editor_frame = self.page.frame_locator("iframe").last
        editor = self.page.locator("#rooster-editor")
        expect(editor).to_be_visible(timeout=15000)
        editor.fill(body)

    def send_email(self):
        self.send_button.click()
