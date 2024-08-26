from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def ask(feedbacks: list, api_key):
    client = OpenAI(api_key=OPENAI_API_KEY)

    content = f"На основе отзывов очень кратко напиши основные (повторяющиеся) плюсы и минусы товара. Максимум 5 плюсов и 5 минусов. Пиши в формате" \
        "json: {'plus': [здесь плюсы и частота встречаемости в скобках], 'minus': [здесь минусы и частота встречаемости в скобках]}. Вот отзывы" + f"{feedbacks}"
    # content_for_gpt4_model = f"На основе URL надйди отзывы и очень кратко напиши основные (повторяющиеся) плюсы и минусы товара. Максимум 5 плюсов и 5 минусов. Пиши в формате" \
    #     "json: {'plus': [здесь плюсы и частота встречаемости в скобках], 'minus': [здесь минусы и частота встречаемости в скобках]}. Вот URL" + f"{feedbacks}"

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
    )
    return chat_completion.choices[0].message.content