import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect

load_dotenv()

email = os.getenv("PROTON_EMAIL")
password = os.getenv("PROTON_PASSWORD")

if not email or not password:
    raise RuntimeError("Set PROTON_EMAIL and PROTON_PASSWORD in .env")

auth_dir = Path("auth")
auth_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://account.proton.me/mail")

    page.get_by_label("Email or username").fill(email)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Sign in").click()

    print("Complete any additional verification in the browser if prompted.")
    input("After your mailbox has fully loaded, press Enter here to save the session...")

    expect(
        page.get_by_role("button", name="New message")
    ).to_be_visible(timeout=15000)

    context.storage_state(path=str(auth_dir / "state.json"))
    print("Authentication state saved locally.")

    browser.close()