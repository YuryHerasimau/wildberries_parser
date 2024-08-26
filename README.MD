# Alfa Seller Interview
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Test task for the position of Python Developer at [Alfa Seller](https://www.youtube.com/channel/UC5PAyF2lhh2vYV4kGeEMUm)


## Description

Необходимо настроить мониторинг негативных отзывов на товары в Wildberries и получать уведомления об этих отзывах в группу Телеграмм.

## Входные данные

Для выполнения задачи необходимо использовать ([файл Excel](files/Книга111.xlsx)) с списком SKU товаров. SKU - это основной идентификатор товаров в Wildberries, который используется, например, в адресе карточки товара: https://www.wildberries.ru/catalog/64245978/detail.aspx

## Содержание уведомления

Уведомление о негативном отзыве должно содержать следующую информацию:
- Негативный отзыв
- Название товара
- SKU товара
- Рейтинг товара (от 4 до 1)
- Текст отзыва
- Текущий рейтинг товара

## Методы мониторинга

Для мониторинга негативных отзывов можно использовать один из следующих методов:
1) Парсинг страниц карточек товара
2) Использование API Wildberries

## Регулярное выполнение задачи

Для регулярного выполнения задачи использован следующий метод запуска:
1) Написан ([скрипт на языке Python](wb_parser.py)), который будет выполнять мониторинг негативных отзывов.
2) Настроен ([запуск скрипта по расписанию](scheduler.py)) с помощью библиотеки schedule.

## Инструменты

Для выполнения задачи использован Python 3.10 и соответствующие библиотеки для парсинга веб-страниц (Selenium, requests, BeautifulSoup).

## Getting Started

### Installing

1. Clone the repository:
```
git clone <repo>
```
2. Install required dependencies:
```
pip install -r requirements.txt
```

### Executing program
Run the script:
```
python wb_parser.py
```
Run the script by schedule:
```
python scheduler.py
```

## What can be improved
- [ ] Cover the code with tests
- [ ] Добавить в уведомление телефон автора отзыва. Метод получения номера телефона неизвестен, но можно попробовать разработать свой метод получения этой информации