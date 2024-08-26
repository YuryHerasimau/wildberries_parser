import requests
import re
import json
from chat_gpt import ask
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
}

class WBReview:
    def __init__(self, string: str):
        self.sku = self.get_sku(string=string)
        self.root_id = self.get_root_id(sku=self.sku)

    @staticmethod
    def get_sku(string: str) -> str:
        """ Get sku from string """
        if "wildberries.ru/catalog/" in string:
            pattern = r"\d{7,15}"
            sku = re.findall(pattern=pattern, string=string)
            if sku:
                return sku[0]
            else:
                raise Exception(f"Can't get sku from string: {string}")

        return string


    def get_root_id(self, sku: str):
        """ Get root_id from sku """
        response = requests.get(
            url=f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-59202&spp=30&ab_testing=false&nm={sku}",
            headers=HEADERS
        )
        if response.status_code != 200:
            raise Exception(f"Can't get root_id from sku: {sku}")
        root_id = response.json()["data"]["products"][0]["root"]
        item_name = response.json()["data"]["products"][0]["name"]
        print(item_name)
        return root_id


    def get_review(self) -> json:
        """ Get reviews from server 1 or 2 """
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
        json_feedback = self.get_review()

        feedbacks = [feedback.get("text") for feedback in json_feedback["feedbacks"]]
        # Чтобы избежать 400й ошибки из-за превышения maximum context lenghth
        if len(feedbacks) > 80:
            feedbacks = feedbacks[:80]
            
        feedback_ratings = [feedback.get("productValuation") for feedback in json_feedback["feedbacks"]]
        average_rating = json_feedback["valuation"]
        feedback_count = json_feedback["feedbackCount"]
        valuation_distributio_percents = json_feedback["valuationDistributionPercent"]

        return feedbacks

if __name__ == "__main__":
    feedbacks = WBReview("https://www.wildberries.ru/catalog/190597734/detail.aspx").parse()
    answer = ask(feedbacks=feedbacks, api_key=OPENAI_API_KEY)
    print(answer)
    # print(WBReview("190597734").sku)
    # print(WBReview("https://www.wildberries.ru/catalog/1/detail.aspx").sku)
