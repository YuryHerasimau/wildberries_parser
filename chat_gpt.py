from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found")


def ask(feedbacks: list, api_key):
    client = OpenAI(api_key=OPENAI_API_KEY)

    content = (
        """Based on the provided reviews, please analyze the feedback and identify the top pros and cons of the product
    in JSON format without any additional text or labels. The format should be strictly.
    For each point, find similar comments, count their occurrences, and include the frequency in parentheses.
    Limit the output to a maximum of 3 main pros and 3 main cons. The final format should be:
    {
        "pros": [
            "Pro 1 (frequency)",
            "Pro 2 (frequency)",
            "Pro 3 (frequency)"
        ],
        "cons": [
            "Con 1 (frequency)",
            "Con 2 (frequency)",
            "Con 3 (frequency)"
        ]
    }
    Please ensure that the analysis is thorough and that only the most relevant points are included.
    Here are the reviews:"""
        + f"{feedbacks}"
    )

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content}],
        )
        print(chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(e)
