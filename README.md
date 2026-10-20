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

## Automation Quality Review

### 1. Which tests did you deliberately choose NOT to automate, and why?

I wouldn't automate everything just for the sake of increasing the test count. CAPTCHA, account recovery that requires external verification, and visual checks that need human judgment are better handled manually. I would also avoid depending on real email delivery in regular UI tests because delivery can be delayed for reasons unrelated to the application. These scenarios still need testing, but manual checks or separate integration tests would be more suitable.

### 2. Which 5 tests would you run on every pull request? Which would you run nightly? Explain the trade-off.

For every pull request, I would run these five checks:

1. Login and authenticated mailbox access.
2. Opening the inbox and verifying that it loads.
3. Opening the compose window and checking required-field validation.
4. Saving a draft and verifying that it can be reopened.
5. Searching for a message using a unique keyword.

These cover important user journeys and should give quick feedback when a change breaks something.

At night, I would run the full suite, including attachment handling, CC/BCC controls, filters, scheduled-send controls, and additional search and draft scenarios. I would also add cross-browser runs when the environment supports them.

The trade-off is execution time versus coverage. Pull request tests should be fast enough to run frequently, while nightly runs can take longer to catch issues across more scenarios. This is the execution strategy I would use as the suite grows.

### 3. How would you diagnose a test that passes locally but fails intermittently in CI?

I would start by checking the failure screenshot, logs, and Playwright trace if available. Then I would compare the local and CI environments, including browser versions, authentication state, test data, and execution speed. I would check whether the test is failing because an element appears late, data is being shared between tests, or the application itself is returning an error. After reproducing the issue, I would fix the cause rather than just increasing timeouts or adding retries.

### 4. How would you reduce test-suite flakiness if the UI changes frequently?

I would use stable locators, such as accessible roles and labels or test IDs, instead of selectors that depend heavily on the page structure. I would keep common interactions in page objects so a locator change can be fixed in one place. I would also use condition-based waits instead of fixed sleeps, assert meaningful outcomes, and make sure tests do not depend on the order in which they run. If a test becomes flaky after a UI change, I would check whether the locator is outdated or the actual behavior has changed before updating the test.

### 5. How would you scale this suite from 20 tests to 200+ tests while keeping maintenance manageable?

I would organize tests by feature, keep shared page interactions and fixtures reusable, and separate test data from test logic. I would group tests into smoke and regression suites so the right tests run at the right time. As the suite grows, I would use API-based setup where appropriate, parallel execution for independent tests, and CI reporting to identify recurring failures and slow tests. I would also review duplicate or low-value tests regularly. The goal would be to add useful coverage without making the suite slow, unreliable, or difficult to maintain.
