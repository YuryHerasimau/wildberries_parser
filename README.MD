# WB Review Parser
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The project is inspired by the content of the YouTube channel [The ParseHub](https://www.youtube.com/@the_parse_hub)


## Description

WB Review Parser — analyzer of positive and negative reviews of Wildberries products by SKU. The SKU is the main product identifier in Wildberries, which is used, for example, in the address of the product card: https://www.wildberries.ru/catalog/64245978/detail.aspx

Below is an example:

<div style="display: flex; justify-content: center; align-items: center;">
    <img src="Screenshot_1.png" width=400 alt="main-screen" />
    <img src="Screenshot_2.png" width=400 alt="result-screen" />
</div>

## Project content

- parsing reviews from Wildberries
- integration with ChatGPT for processing reviews
- adding a cross-platform graphical interface

## Getting Started

### Installing

1. Clone the repository:
```
git clone https://github.com/YuryHerasimau/wildberries_parser.git
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Сreate a `.env` file in the root directory with your OPENAI_API_KEY

### Executing program
Run as a desktop app:
```
flet run
```
Run as web app:
```
flet run --web --port 8000
```

## What can be improved
- [x] Add the product name to the UI, as well as other data such as average rating and number of reviews
- [ ] Compile the entire program into an exe file
- [ ] Cover the code with tests
