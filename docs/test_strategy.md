# Proton Mail Web — Test Strategy

## 1. Objective

Validate the primary Proton Mail web workflows, including authentication, composing messages, draft persistence, inbox actions, search, filters, asynchronous send cancellation, and attachments.

## 2. Scope

**In scope**
- Sign-in form validation
- Compose window and message validation
- Draft creation and persistence
- Inbox message actions
- Basic and advanced search
- Filter creation and behavior
- Undo Send, where enabled
- Attachment selection and display

**Out of scope**
- Bypassing CAPTCHA or anti-abuse controls
- Testing with unauthorized accounts
- Production load testing
- Confirming delivery through external email providers without a controlled recipient account

## 3. Test Approach

Use risk-based testing. Prioritize authentication, message composition, draft persistence, and search because failures in these workflows can prevent users from accessing or managing email.

Use Python, Pytest, and Playwright with page objects to separate UI interactions from test assertions. Use role-based locators where available and stable element IDs where verified.

## 4. Test Data and Environment

- Browser: Chromium
- Environment: Proton Mail web application
- Accounts: Authorized assessment account only
- Message subjects: Unique, timestamped values
- Attachments: Small, harmless sample files
- Credentials: Environment variables; never hard-coded

## 5. Execution Strategy

- Run public sign-in validation tests independently.
- Reuse an existing authenticated session for mailbox tests when permitted.
- Run focused tests during development.
- Run the full regression suite when authentication and test data are available.
- Use condition-based waits instead of arbitrary sleeps.
- Capture screenshots and traces for failures.

## 6. Entry Criteria

- Dependencies are installed.
- The application is reachable.
- Required test data is available.
- An authorized session is available for authenticated tests.

## 7. Exit Criteria

- Planned test cases have documented results.
- Critical failures are investigated.
- Known limitations and skipped tests are recorded.
- No unverified defect is reported as confirmed.
- Test results and supporting evidence are available.

## 8. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Anti-abuse restrictions from repeated sign-ins | Reuse a permitted session and avoid repeated authentication |
| UI changes break selectors | Prefer accessible locators and centralize selectors in page objects |
| Session expires | Detect the sign-in redirect and report a blocked test clearly |
| Email tests create side effects | Use controlled test data and send only when necessary |
| Flaky asynchronous behavior | Wait for observable application state and use bounded timeouts |
