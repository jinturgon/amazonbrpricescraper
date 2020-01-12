import requests 
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from product import Product

from colorama import init, Fore, Back, Style
from termcolor import colored
init(convert=True, autoreset=True)

searchTerm = str(input("O que você está procurando?\n:"))

products = []

def convert_price_toNumber(price: str) -> float:
    """Convert the string price to float
    and remove symbols from it
    :param price: A str holding price
    :returns: Price in float
    """
    price = price.split("$")[1]
    try:
        price = price.split(",")[0].replace('.','') + "." + price.split(",")[1]
    except:
        price = price.split(",")[0] + "." + price.split(",")[1]

    return float(price)

pageNumber = 1
while pageNumber != 12:
        URL = "http://www.amazon.com.br/s?k=" + searchTerm
        URL = URL + '&page=' + str(pageNumber)
        print("Page nº: " + str(pageNumber))
        print(URL)

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        eraseReviews = soup.find_all('div', class_='a-section a-spacing-none a-spacing-top-micro')
        for element in eraseReviews:
            element.decompose()

        # produtos_box_lista = soup.find(class_='a-section a-spacing-medium')
        productsBox = soup.find_all('div', class_='a-section a-spacing-medium')
        productsBoxConcatenate = '<br/>'.join([str(tag) for tag in productsBox])
        productsBox = BeautifulSoup(productsBoxConcatenate, 'html.parser')


        decomposeIrrelevant = productsBox.find_all('span', class_='rush-component') + productsBox.find_all('div', class_='a-section a-spacing-none') + productsBox.find_all('div', class_='a-section a-spacing-none a-spacing-top-mini') + productsBox.find_all('a', class_='a-size-base a-link-normal') + productsBox.find_all('a', class_='a-link-normal a-text-normal') + productsBox.find_all('a', class_='a-size-base a-link-normal a-text-bold')
        for element in decomposeIrrelevant:
            element.decompose()

        productsBoxItem = productsBox.find_all('a')

        for item in productsBoxItem:
            shouldAdd = True
            name, link, price, prevPrice, discount = '', '', '', '', ''

            try:
                name = item.get('href').split('/')[1].replace('-',' ')
                link = 'http://www.amazon.com.br' + item.get('href')
                price = convert_price_toNumber(item.find(class_='a-price').find(class_='a-offscreen').contents[0])
                try:
                    prevPrice = convert_price_toNumber(item.find(class_='a-price a-text-price').find(class_='a-offscreen').contents[0])
                    discount = float(round(((prevPrice - price)*100)/prevPrice,2))
                except:
                    prevPrice = price
                    discount = 0.0
                # print(Fore.GREEN + str(item))
                print(Fore.GREEN + "Success!")
            except:
                Exception()
                # print(Fore.RED + str(item))
                print(Fore.RED + "Exception.")
                shouldAdd = False
            product = Product(name, price, prevPrice, discount, link)
            if shouldAdd:
                products.append(product)

        pageNumber += 1

biggest_discount = 0.0
lowest_price = 0.0
chepest_product = Product("", "", "", "", "")
best_deal_product = Product("", "", "", "", "")
searchTerms = searchTerm.split(" ")

run = 0

for product in products:
    not_right = False
    for word in searchTerms:
        if word.lower() not in product.name.lower():
            not_right = True
    if not not_right:
        if run == 0:
            lowest_price = product.price
            chepest_product = product
            run = 1
        elif product.price < lowest_price:
            lowest_price = product.price
            chepest_product = product
        discount = product.prevPrice - product.price
        if discount > biggest_discount:
            biggest_discount = discount
            best_deal_product = product

with open('products.json', 'w') as json_file:
    data = {}
    data["Products"] = []
    for prod in products:
        data["Products"].append(prod.serialize())
    json.dump(data, json_file, sort_keys=True, indent=4)

print(json.dumps(chepest_product.serialize(), indent=4, sort_keys=True))
print(json.dumps(best_deal_product.serialize(), indent=4, sort_keys=True))

print(Fore.BLUE + "\n Product list size: ", end='');print(len(products))


# chromedriverPATH = ""
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# driver = webdriver.Chrome(chromedriverPATH, options=options)
# driver.get(best_deal_product.link)