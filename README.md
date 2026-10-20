# Proton Mail Web — QA Automation Assessment

## Overview

This project tests selected Proton Mail web workflows using Python, Playwright, Pytest, and the Page Object Model (POM).

## Scope

- Authentication form validation
- Compose-window and message-field checks
- Inbox accessibility
- Draft persistence
- Search workflows
- Additional filter, attachment, and asynchronous-send scenarios documented for assessment coverage

The detailed scenario inventory is in `docs/test_cases.md`.

The test approach is in `docs/test_strategy.md`.

The design rationale is in `docs/architecture.md`.

## Tech Stack

- Python
- Playwright
- Pytest
- pytest-html
- python-dotenv

## Setup

Clone the repository and navigate to the project directory.

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies and the Chromium browser:

```bash
pip install -r requirements.txt
playwright install chromium
```

### Configure Credentials

Create a local `.env` file in the project root:

```env
PROTON_EMAIL=your_authorized_test_account
PROTON_PASSWORD=your_password
```

Replace the placeholders with credentials for an authorized test account. The variable names must match those read by the authentication setup script.

Never commit `.env`, passwords, cookies, or authentication state.

## Authentication Setup

Authenticated tests use a locally saved Playwright browser state at `auth/state.json`. This file is intentionally excluded from version control because it may contain session cookies and other sensitive authentication information.

After configuring `.env`, generate the authentication state:

```bash
python save_auth_state.py
```

A browser opens so you can complete authentication manually. Follow any additional steps required by the account. The script saves the resulting browser state locally if authentication succeeds.

You normally do not need to run this setup script before every test. Reuse the saved state while it remains valid. If the session expires or the state file is missing or invalid, rerun the setup script and authenticate again.

Each person cloning the repository must create their own `.env` file and authentication state. Your local credentials and session are not included in the repository.

**Security notes:**
- Never commit `.env` or `auth/state.json`.
- Never share or upload the authentication state file.
- Use only an authorized test account and permitted test data.
- Treat the saved session as sensitive even though it does not contain a plain-text password by design.

## Running Tests

Collect the available tests without executing them:

```bash
python -m pytest --collect-only -q
```

Run the complete suite:

```bash
python -m pytest -v
```

Run the suite and generate a self-contained HTML report:

```bash
python -m pytest -q --html=reports/pytest-report.html --self-contained-html
```

Run a focused test file:

```bash
python -m pytest tests/test_inbox.py -v
```

Review the terminal summary and HTML report for actual results. A collected test is not necessarily an implemented or passing test. Investigate failures and skips before reporting coverage.

## CI vs Nightly

Run a small, stable smoke suite on every pull request to provide fast feedback. Run the broader regression suite nightly or before a release.

The trade-off is faster pull-request feedback versus wider coverage at a higher execution cost. Tests that send messages or change mailbox data should use controlled test data and a dedicated authorized account.

## Diagnosing CI-Only Failures

1. Compare browser, Python, dependency, and environment versions.
2. Inspect screenshots, Playwright traces, logs, and the HTML report.
3. Determine whether the failure involves a locator, timing, test-data dependency, or environment/configuration difference.
4. Reproduce the failure with the same browser and configuration.
5. Fix the underlying cause instead of adding arbitrary sleeps or retries.

## Reducing UI-Test Flakiness

Prefer accessible roles and labels or stable test IDs. Keep locators in page objects, wait for observable application states, isolate test data, and avoid fixed sleeps.

Use bounded retries only for understood transient failures. Do not use retries to hide genuine defects.

## Scaling from 20 to 200+ Tests

Organize tests by feature, keep reusable page objects and fixtures, externalize test data, and tag smoke and regression tests.

Use isolated test data, parallel execution where safe, CI artifacts, and a consistent reporting strategy. Avoid sharing mutable mailbox state between parallel tests.

## Limitations

Some workflows require known test messages, verified UI selectors, or careful control of side effects. CAPTCHA, account recovery, visual/usability judgement, and external delivery verification may require manual testing.

Tests that send real messages, schedule delivery, or modify mailbox data should be implemented only with authorized accounts and controlled test data. Only confirmed, reproducible observations should be reported as defects.

## Current Status

The latest reported full test run passed. The subsequent collection-only command confirmed that **10 tests are currently collected**.

These results describe the current automated suite only; they do not establish that every workflow listed in the assessment scope has been automated or tested. Review the latest test report before submission.
