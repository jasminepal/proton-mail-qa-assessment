import pytest
from playwright.sync_api import expect


@pytest.mark.skip(
    reason="Requires verified search locator and authenticated test session"
)
def test_search_returns_matching_messages(authenticated_page):
    page = authenticated_page

    # Replace with the verified search locator after inspecting the UI.
    search_box = page.get_by_role("searchbox")
    search_box.fill("assessment-search-term")
    search_box.press("Enter")

    # Add an assertion for a known matching message here.
    expect(search_box).to_be_visible()