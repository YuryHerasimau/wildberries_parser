import requests
import re
import json
from gpt_api import ask
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
}


class WBReview:
    def __init__(self, string: str):
        self.sku = self.get_sku(string=string)
        self.root_id = self.get_root_id(sku=self.sku)
        self.item_name = self.get_item_name(sku=self.sku)

    @staticmethod
    def get_sku(string: str) -> str:
        """Get sku from string"""
        if "wildberries.ru/catalog/" in string:
            pattern = r"\d{7,15}"
            sku = re.findall(pattern=pattern, string=string)
            if sku:
                return sku[0]
            else:
                raise Exception(f"Can't get sku from string: {string}")

        return string

    def get_root_id(self, sku: str):
        """Get root_id from sku"""
        response = requests.get(
            url=f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-59202&spp=30&ab_testing=false&nm={sku}",
            headers=HEADERS,
        )
        if response.status_code != 200 or not response.json()["data"]["products"]:
            raise Exception(f"Can't get root_id from sku: {sku}")
        root_id = response.json()["data"]["products"][0]["root"]
        return root_id

    def get_item_name(self, sku: str):
        """Get item_name from sku"""
        response = requests.get(
            url=f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-59202&spp=30&ab_testing=false&nm={sku}",
            headers=HEADERS,
        )
        if response.status_code != 200:
            raise Exception(f"Can't get item_name from sku: {sku}")
        item_name = response.json()["data"]["products"][0]["name"]
        return item_name

    def get_review(self) -> json:
        """Get reviews from server 1 or 2"""
        try:
            response = requests.get(
                url=f"https://feedbacks1.wb.ru/feedbacks/v1/{self.root_id}",
                headers=HEADERS,
            )
            if response.status_code == 200:
                if not response.json()["feedbacks"]:
                    raise Exception("Server 1 is not suitable")
                return response.json()
        except Exception as e:
            response = requests.get(
                url=f"https://feedbacks2.wb.ru/feedbacks/v1/{self.root_id}",
                headers=HEADERS,
            )
            if response.status_code == 200:
                return response.json()

    def parse(self):
        json_feedbacks = self.get_review()
        # Added sku filter to ("Этот вариант товара")
        feedbacks = [
            feedback.get("text")
            for feedback in json_feedbacks["feedbacks"]
            if str(feedback.get("nmId")) == self.sku
        ]
        # To avoid 400 error due to exceeding maximum context length
        if len(feedbacks) > 80:
            feedbacks = feedbacks[:80]

        feedback_ratings = [feedback.get("productValuation") for feedback in json_feedbacks["feedbacks"]]  # TO DO
        average_rating = json_feedbacks["valuation"]
        feedback_count = json_feedbacks["feedbackCount"]
        valuation_distribution_percents = json_feedbacks["valuationDistributionPercent"]  # TO DO
        return feedbacks, average_rating, feedback_count


if __name__ == "__main__":
    # "https://www.wildberries.ru/catalog/190597734/detail.aspx"
    feedbacks = WBReview(input("Enter the product URL or SKU code: ")).parse()
    answer = ask(feedbacks=feedbacks, api_key=OPENAI_API_KEY)
    print(answer)
