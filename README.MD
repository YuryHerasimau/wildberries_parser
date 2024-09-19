# WB Review Parser

WB Review Parser is ...


## Description

WB Review Parser — analyzer of positive and negative reviews of Wildberries products by SKU. The SKU is the main product identifier in Wildberries, which is used, for example, in the address of the product card: https://www.wildberries.ru/catalog/64245978/detail.aspx

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
Run the script:
```
flet run [main.py]
```

## What can be improved
- [ ] Add the product name to the UI, as well as other data such as average rating and number of reviews
- [ ] Compile the entire program into an exe file
- [ ] Cover the code with tests
