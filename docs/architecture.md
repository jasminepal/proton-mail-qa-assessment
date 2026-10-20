# Automation Architecture

## Design
The suite uses Pytest for test execution and fixtures, Playwright for browser
automation, and page objects to separate UI operations from test assertions.

- `pages/`: page objects and reusable UI interactions.
- `tests/`: feature-level test scenarios and assertions.
- `conftest.py`: shared fixtures and failure evidence.
- `test_data/`: non-secret test data.
- `docs/`: strategy, scenario inventory, and architecture.
- `reports/`: generated reports and evidence; excluded from Git.

## Authentication
`save_auth_state.py` creates a local Playwright storage-state file after
manual authentication. The `authenticated_page` fixture loads that state
into a fresh browser context. It avoids repeatedly submitting the login
form but does not guarantee the session remains valid.

The state file is sensitive and must not be committed.

## Reliability
Use accessible locators, bounded expect assertions, isolated browser contexts,
and deterministic test data. Capture screenshots on failures. Add traces
when debugging timing or browser-specific failures.

## Test Execution Strategy
Run fast, stable smoke checks on pull requests. Run broader regression
coverage on a schedule or before releases. Tests that alter mailbox contents
or send email require controlled data and should not run concurrently against
shared mutable messages.

## Current Limitations
Not all documented scenarios have been implemented or verified. Search,
filters, attachments, draft persistence, and undo-send require validated
locators and controlled test data before being considered complete.
