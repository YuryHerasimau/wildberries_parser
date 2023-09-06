import requests
import time
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_product_id():
    excel_data = pd.read_excel("Книга111.xlsx", header=None)
    id_list = excel_data[0].tolist()
    return id_list


def get_product_info(url:str, id:str):
    pattern = '(?<=catalog\/).+(?=\/)'
    product_id = re.search(pattern, url)[0]

    # get product info
    response = requests.get(f'https://card.wb.ru/cards/detail?nm={product_id}')
    result = []
    result.append({
        'name': response.json()['data']['products'][0]['brand'] + ' / ' + response.json()['data']['products'][0]['name'], # название товара
        'id': response.json()['data']['products'][0]['id'], # SKU товара
        'reviewRating': response.json()['data']['products'][0]['reviewRating'] # Текущий рейтинг товара
    })

    # set up webdriver and get feedbacks
    imt_id = response.json()['data']['products'][0]['root']
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get(url=f'https://www.wildberries.ru/catalog/{product_id}/feedbacks?imtId={imt_id}')
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Pause while the page is loading
            time.sleep(2)
            # Calculate the new scroll height and compare with the highest scroll height
            new_height = driver.execute_script("return document.body.scrollHeight") 
            if new_height == last_height:
                print("Scroll completed")
                driver.find_elements(By.CLASS_NAME, "comments__list")
                with open("source-page.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break 
            else:
                last_height = new_height
                print("New content has arrived, keep scrolling")
        
            time.sleep(3)


        with open("source-page.html", "r", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        comments = soup.find_all(class_='feedback__text')
        authors = soup.find_all(class_='feedback__header')
        rating = soup.find_all(class_='feedback__rating') # class='feedback__rating stars-line star4'

        for i in range(0, len(comments)):
            stars_str = rating[i].attrs.get('class')[2] # 'feedback__rating stars-line star4' -> 'star4'
            stars_num = int(stars_str.split("star")[1]) # 'star4' -> 4
            if stars_num <= 4:
                result.append({
                    'feedback': comments[i].text, # текст отзыва
                    'rating': stars_num, # столько-то звезд (от 4х до 1ой)
                })

    except Exception as _ex:
        print(_ex)
        
    finally:
        driver.close()
        driver.quit()
    
    save_to_json(result=result, id=id)


def save_to_json(result:list, id:str):
    with open(f"{id}_wb_data.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    ids = get_product_id()
    for id in ids:
        url = 'https://www.wildberries.ru/catalog/' + str(id) + '/detail.aspx'
        get_product_info(url=url, id=id)
    

if __name__ == "__main__":
    main()