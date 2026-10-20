def test_proton_mail_page_opens(page):
    page.goto("https://proton.me/mail")

    assert page.title()
    print("Page title:", page.title())