# Proton Mail Web — Test Cases

## Test Environment
- Application: https://mail.proton.me/
- Framework: Python, Playwright, Pytest
- Browser: Chromium
- Test type: UI functional and regression testing
- Test account: Authorized assessment account
- Execution note: Authenticated scenarios require a valid session. Do not repeatedly authenticate during development.

| ID | Scenario | Priority | Type | Expected Result |
|---|---|---|---|---|
| AUTH-01 | Open the sign-in page | P1 | Automate | Sign-in form is displayed |
| AUTH-02 | Submit empty sign-in fields | P1 | Automate | Required-field validation is shown |
| AUTH-03 | Sign in with invalid credentials | P1 | Automate | Authentication is rejected without opening the mailbox |
| INB-01 | Open the authenticated inbox | P1 | Automate | Inbox loads and message controls are available |
| INB-02 | Open a message from the inbox | P1 | Automate | The selected message content is displayed |
| INB-03 | Mark a message as unread | P2 | Automate | The message is marked unread |
| INB-04 | Move a message to Trash | P2 | Automate | The message is removed from the inbox and appears in Trash |
| CMP-01 | Open the compose window | P1 | Automate | Recipient, subject, body editor, and Send controls are available |
| CMP-02 | Compose a message with a recipient, subject, and body | P1 | Automate | All entered values are displayed correctly |
| CMP-03 | Attempt to send without a recipient | P1 | Automate | Message is not sent and recipient validation is presented |
| CMP-04 | Open the CC recipient control | P2 | Automate | CC recipient field is displayed |
| CMP-05 | Open the BCC recipient control | P2 | Automate | BCC recipient field is displayed |
| DRF-01 | Save a message as a draft | P1 | Automate | Draft is saved and appears in Drafts |
| DRF-02 | Reopen a saved draft | P1 | Automate | Previously entered content is retained |
| DRF-03 | Reopen a draft and verify its subject persists | P1 | Automate | Previously saved subject is retained |
| SRC-01 | Search using a unique keyword | P1 | Automate | Matching messages are returned |
| SRC-02 | Search using multiple available criteria | P2 | Automate | Results satisfy the selected search criteria |
| FLT-01 | Open the inbox filter options | P2 | Automate | Filter options are displayed |
| ASY-01 | Open scheduled-send options | P2 | Automate | Scheduled-send options are displayed |
| ASY-02 | Verify Undo Send, if available in account settings | P2 | Manual / conditional | Sending can be cancelled within the configured undo window |
| ATT-01 | Attach a permitted test file to a draft | P1 | Automate | The selected file appears as an attachment in the composer |
| ATT-02 | Attach multiple files to a draft | P1 | Automate | Both selected filenames appear in the composer |


## Manual and Non-Automated Coverage

| Scenario | Classification | Reason |
|---|---|---|
| CAPTCHA or anti-abuse challenge | Manual | May require human interaction and should not be bypassed |
| Recovery through a second factor | Manual | Depends on account security configuration |
| Visual layout and usability review | Manual | Human judgement is useful for visual quality |
| Real-world email delivery across external providers | Manual / integration test | Requires controlled external accounts and delivery verification |
| Large-scale attachment and quota limits | Manual / specialized test | Requires controlled test data and careful resource management |
| Successful scheduled delivery at the selected time | Manual / integration test | Requires controlled scheduling and verification of delivery |

## Execution Rules
1. Use only authorized test accounts and test data.
2. Keep credentials and authentication state out of version control.
3. Reuse an authenticated session for UI tests where supported.
4. Use explicit Playwright assertions and condition-based waits.
5. Capture screenshots and traces for failures.
6. Record actual results only after executing the test.
7. Do not report a suspected issue as a confirmed defect without reproducible evidence.

**Priority definitions:** P1 = high business impact; P2 = medium impact. P0 and P3 can be assigned when the assessed risk justifies them.