import flet as ft
from wb_parser import WBReview
from chat_gpt import ask
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path=".env")

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
        submit_btn.disabled = len(url_input.value) < 7
        page.update()

    # Parsing function
    def parse(e):
        loading_text.visible = True  # Show loader
        page.update()  # Update the page to show the loader

        try:
            feedbacks, average_rating, feedback_count = WBReview(string=url_input.value).parse()
            item_name = WBReview(string=url_input.value).item_name
            if feedbacks:
                result_gpt = ask(feedbacks=feedbacks, api_key=OPENAI_API_KEY)
                additional_info = (
                    f"Товар: {item_name}\n"
                    f"Средняя оценка: {average_rating}\n"
                    f"Количество отзывов: {feedback_count}\n"
                )
                update_dialog_text(
                    json_response=result_gpt, additional_info=additional_info
                )
            else:
                update_dialog_text("No reviews found for this URL. Try another one.")
        except Exception as ex:
            update_dialog_text(
                f"Something went wrong. Try again later. \n\nError message: {ex}"
            )
        finally:
            loading_text.visible = False  # Hide loader after processing
            page.update()  # Update the page again to hide the loader

    # Update dialog text and open dialog
    def update_dialog_text(json_response, additional_info=None):
        # Remove triple quotes if present at the beginning and end
        if json_response.startswith("```") and json_response.endswith("```"):
            json_response = json_response[3:-3].strip()
            print(f"json_response[3:-3].strip(): {json_response}")

        # Clean the response if it contains the word "json" at the beginning
        if json_response.strip().startswith("json"):
            json_response = json_response[4:].strip()
            print(f"json_response[4:].strip(): {json_response}")

        # Check if the response is empty or consists only of whitespace
        if not json_response.strip():
            alert_dialog.title = ft.Text("Error: Received empty response.")
            page.open(alert_dialog)
            return  # Exit if the response is empty

        try:
            data = json.loads(json_response)  # Load the JSON data
        except json.JSONDecodeError as ex:
            alert_dialog.title = ft.Text(
                "Error: Invalid JSON format. Details: " + str(ex)
            )
            page.open(alert_dialog)
            return  # Exit if there's an error in JSON decoding

        # Proceed only if data is valid
        if data:
            # Create formatted text for pros and cons
            plus_text = "\n".join([f"• {item}" for item in data.get("pros", [])])
            minus_text = "\n".join([f"• {item}" for item in data.get("cons", [])])

            # Set the alert dialog title with formatted text. Include additional info if provided
            formatted_text = (
                f"{additional_info}\nПлюсы:\n{plus_text}\n\nМинусы:\n{minus_text}"
                if additional_info
                else f"Плюсы:\n{plus_text}\n\nМинусы:\n{minus_text}"
            )
            alert_dialog.title = ft.Text(formatted_text)
            page.open(alert_dialog)
        else:
            alert_dialog.title = ft.Text(
                "No reviews found for this URL or article code. Try another one."
            )
            page.open(alert_dialog)

    # Close dialog
    def handle_close(e):
        page.close(alert_dialog)

    # Input field and button creation
    url_input = ft.TextField(
        label="Paste the product URL or article code (SKU)", width=700, on_change=check_input
    )
    submit_btn = ft.FilledButton(text="Start", width=150, disabled=True, on_click=parse)

    # Loader setup
    loading_text = ft.Text("Loading...", visible=False)

    # Alert dialog setup
    alert_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Review Summary"),
        actions=[
            ft.TextButton("OK", on_click=handle_close),
        ],
    )

    # Add components to the page
    page.add(ft.Row([url_input], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([submit_btn], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([loading_text], alignment=ft.MainAxisAlignment.CENTER))

    # Final page update
    page.update()


ft.app(target=main)
