from playwright.sync_api import expect


def test_filter_controls_are_available(authenticated_page):
    page = authenticated_page
    page.goto("https://mail.proton.me/u/1/inbox")

    filter_button = page.get_by_test_id("filter-dropdown:show-filters")
    expect(filter_button).to_be_visible()
    filter_button.click()

    # Verify that opening the filter control exposes a UI panel.
    panels = page.locator('[role="dialog"], [role="menu"], [role="listbox"]')
    expect(panels.first).to_be_visible(timeout=5000)