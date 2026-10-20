from playwright.sync_api import expect


def test_search_returns_matching_messages(authenticated_page):
    page = authenticated_page
    page.goto("https://mail.proton.me/u/1/inbox")

    # Open the search panel and enter a keyword from the existing email.
    page.get_by_test_id("search-keyword").click()

    search_input = page.get_by_placeholder(
        "Search date, name, email address, or subject line"
    )
    search_input.fill("Gmail")

    # Submit the search from the opened panel.
    page.get_by_role("button", name="Search", exact=True).last.click()

    # Verify that the matching email appears in the results.
    expect(
        page.get_by_text(
            "Move from Gmail in one click, bring everything to Proton",
            exact=False,
        )
    ).to_be_visible(timeout=15000)