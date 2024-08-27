from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found")


def ask(feedbacks: list, api_key):
    client = OpenAI(api_key=OPENAI_API_KEY)

    content = f"Based on the reviews, briefly summarize the main (reoccurring) pros and cons of the product."\
    "Limit to a maximum of 5 pros and 5 cons. Format your response in JSON:"\
    "{'plus': [pros with their frequency in parentheses], 'minus': [cons with their frequency in parentheses]}"\
    "Here are the reviews:" + f"{feedbacks}"

    # content_for_gpt4_model = f"На основе URL надйди отзывы и очень кратко напиши основные (повторяющиеся) плюсы и минусы товара. Максимум 5 плюсов и 5 минусов. Пиши в формате" \
    #     "json: {'plus': [здесь плюсы и частота встречаемости в скобках], 'minus': [здесь минусы и частота встречаемости в скобках]}. Вот URL" + f"{feedbacks}"

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content