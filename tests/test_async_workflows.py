from playwright.sync_api import expect
from pages.compose_page import ComposePage


def test_scheduled_send_control_is_available(authenticated_page):
    page = authenticated_page
    page.goto("https://mail.proton.me/u/1/inbox")

    compose = ComposePage(page)
    compose.open_composer()

    scheduled_send = page.get_by_test_id(
        "composer:scheduled-send:open-dropdown"
    )
    expect(scheduled_send).to_be_visible()
    scheduled_send.click()

    # Verify that the scheduled-send menu or dialog opens.
    overlays = page.locator(
        '[role="dialog"], [role="menu"], [role="listbox"]'
    )
    expect(overlays.first).to_be_visible(timeout=5000)