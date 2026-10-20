from pathlib import Path

import pytest

AUTH_STATE = Path("auth/state.json")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = (
            item.funcargs.get("page")
            or item.funcargs.get("authenticated_page")
        )

        if page:
            evidence_dir = Path("reports/screenshots")
            evidence_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = evidence_dir / f"{item.name}.png"

            try:
                page.screenshot(
                    path=str(screenshot_path),
                    full_page=True,
                )
                print(f"\nFailure screenshot: {screenshot_path}")
            except Exception as error:
                print(f"\nCould not capture screenshot: {error}")


@pytest.fixture
def authenticated_page(browser):
    """Reuse a local saved session without submitting the login form."""
    if not AUTH_STATE.is_file():
        pytest.skip(
            "No saved session found. Run save_auth_state.py when access is available."
        )

    context = browser.new_context(storage_state=str(AUTH_STATE))
    page = context.new_page()

    try:
        yield page
    finally:
        context.close()
