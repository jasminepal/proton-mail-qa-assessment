from playwright.sync_api import Page, expect


class DraftsPage:
    def __init__(self, page: Page):
        self.page = page

    def verify_draft_saved(self):
        # Call only after the UI confirms the draft was saved.
        expect(
            self.page.get_by_text("Draft", exact=False).first
        ).to_be_visible(timeout=15000)