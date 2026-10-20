from pathlib import Path

from playwright.sync_api import expect
from pages.compose_page import ComposePage


def test_user_can_attach_a_file_to_a_draft(authenticated_page, tmp_path):
    page = authenticated_page
    page.goto("https://mail.proton.me/u/1/inbox")

    compose = ComposePage(page)
    compose.open_composer()

    attachment = tmp_path / "qa-attachment.txt"
    attachment.write_text("Temporary attachment for QA testing.")

    page.get_by_test_id("composer-attachments-button").set_input_files(
        str(attachment)
    )

    # Verify the uploaded file is represented in the composer.
    expect(
        page.get_by_text("qa-attachment.txt", exact=True).first
    ).to_be_visible(timeout=10000)
    
    

def test_multiple_files_can_be_attached_to_a_draft(
    authenticated_page, tmp_path
):
    page = authenticated_page
    page.goto("https://mail.proton.me/u/1/inbox")

    compose = ComposePage(page)
    compose.open_composer()

    first_file = tmp_path / "qa-file-one.txt"
    second_file = tmp_path / "qa-file-two.txt"

    first_file.write_text("First temporary QA attachment.")
    second_file.write_text("Second temporary QA attachment.")

    page.get_by_test_id("composer-attachments-button").set_input_files(
        [str(first_file), str(second_file)]
    )

    expect(
        page.get_by_text("qa-file-one.txt", exact=True).first
    ).to_be_visible(timeout=10000)

    expect(
        page.get_by_text("qa-file-two.txt", exact=True).first
    ).to_be_visible(timeout=10000)
