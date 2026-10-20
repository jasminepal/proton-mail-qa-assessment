from playwright.sync_api import expect


def test_search_returns_matching_messages(authenticated_page):
    authenticated_page.goto("https://mail.proton.me/u/1/inbox")

    search = authenticated_page.get_by_test_id("search-keyword")

    print("\n--- Search input ---")
    print(search.evaluate("(el) => el.outerHTML"))

    print("\n--- Search input parent ---")
    print(search.locator("xpath=..").evaluate("(el) => el.outerHTML"))

    print("\n--- Search button ---")
    button = authenticated_page.get_by_role("button", name="Search")
    print(button.evaluate("(el) => el.outerHTML"))