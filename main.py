import flet as ft
from wb_parser import WBReview
from chat_gpt import ask
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found")


def main(page: ft.Page):
    # Page setup
    page.title = "Wildberries Reviews"
    page.theme_mode = "dark"
    page.window.width = 900
    page.window.height = 900
    page.window.resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Input validation function
    def check_input(e):
        # if len(url_input.value) >= 7:
        #     submit_btn.disabled = False
        # else:
        #     submit_btn.disabled = True
        submit_btn.disabled = len(url_input.value) < 7
        page.update()

    # Parsing function
    def parse(e):
        try:
            feedbacks = WBReview(string=url_input.value).parse()
            if feedbacks:
                result_gpt = ask(feedbacks=feedbacks, api_key=OPENAI_API_KEY)
                change_text_in_dialog(result_gpt)
            else:
                change_text_in_dialog("No reviews found for this URL. Try another one.")
        except Exception as ex:
            print(f"Error: {ex}")

    # # Update dialog text and open dialog
    def change_text_in_dialog(text):
        alert_dialog.title = ft.Text(text)
        page.open(alert_dialog)
        # page.update()

    # # Close dialog
    def handle_close(e):
        page.close(alert_dialog)
        # page.update()

    # Input field and button creation
    url_input = ft.TextField(label="Paste the product URL or article code", width=700, on_change=check_input)
    submit_btn = ft.FilledButton(text="Start", width=150, disabled=True, on_click=parse)

    # Alert dialog setup
    alert_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Result"),
        actions=[
            ft.TextButton("OK", on_click=handle_close),
        ]
    )
    
    # Add components to the page
    page.add(ft.Row([url_input], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([submit_btn], alignment=ft.MainAxisAlignment.CENTER))

    page.update()


ft.app(target=main)