# Proton Mail Web — QA Automation Assessment

## Overview
This project tests selected Proton Mail web workflows using Python,
Playwright, Pytest, and the Page Object Model (POM).

## Scope
- Authentication form validation
- Compose-window and message-field checks
- Inbox accessibility
- Draft persistence
- Search and filter workflows
- Attachments and asynchronous send behavior

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
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Create a local `.env` file only if a test requires credentials:
```text
PROTON_EMAIL=your_authorized_test_account
PROTON_PASSWORD=your_password
```

Never commit `.env`, authentication state, cookies, or passwords.

## Authentication
For authenticated UI tests, the project supports a locally saved
Playwright state at `auth/state.json`.

Create it using `python save_auth_state.py` and complete authentication
manually in the visible browser. The session can expire and may need to
be refreshed. Never upload the state file.

## Running Tests
Collect tests without executing them:
```bash
python -m pytest --collect-only -q
```

Run the suite and generate an HTML report:
```bash
python -m pytest -q --html=reports/pytest-report.html --self-contained-html
```

Run a focused test:
```bash
python -m pytest tests/test_inbox.py -v
```

Skipped tests must be reviewed before reporting coverage. A collected
test is not necessarily an implemented or passing test. Check the
terminal summary and HTML report for actual results.

## CI vs Nightly
Run a small, stable smoke suite on every pull request to give fast feedback.
Run the broader regression suite nightly or before a release. The trade-off
is faster pull-request feedback versus wider coverage at a higher execution
cost. Tests that send messages or change mailbox data should use controlled
test data and a dedicated authorized account.

## Diagnosing CI-Only Failures
1. Compare browser, Python, dependency, and environment versions.
2. Inspect screenshots, Playwright traces, logs, and the HTML report.
3. Check whether the failure is a locator issue, timing issue, test-data
   dependency, or environment/configuration difference.
4. Reproduce with the same browser and configuration.
5. Fix the underlying cause instead of adding arbitrary sleeps or retries.

## Reducing UI-Test Flakiness
Prefer accessible roles and labels or stable test IDs. Keep locators in
page objects, wait for observable state, isolate test data, and avoid
fixed sleeps. Use bounded retries only for understood transient failures;
do not use retries to hide genuine defects.

## Scaling from 20 to 200+ Tests
Organize tests by feature, keep reusable page objects and fixtures,
externalize test data, and tag smoke/regression tests. Use isolated data,
parallel execution where safe, CI artifacts, and a consistent reporting
strategy. Avoid shared mutable mailbox state between parallel tests.

## Limitations
Some workflows require known test messages, verified UI selectors, or
careful control of side effects. CAPTCHA, account recovery, visual/usability
judgement, and external delivery verification may require manual testing.
Only confirmed, reproducible observations should be reported as defects.

## Current Status
Test execution status must be taken from the latest actual pytest run.
The project has previously collected 10 tests, with 4 passing and 6
skipped; the authenticated inbox test subsequently passed independently.
These are historical results, not a claim that the final suite has passed.
