from bs4 import BeautifulSoup
import requests
import csv

class product:
    def __init__(self, name="", price="", link="", sku="",img_url=""):
        self.name = name
        self.price = price
        self.link = link
        self.sku = sku
        self.img_url = img_url
    def __str__(self):
        return f"{self.name},{self.price},{self.link},{self.sku},{self.img_url}\n"


root_url = "https://www.amway.com/en_US/Shop/Nutrition/Vitamins-&-Supplements/c/124/results?pageSize=100&page=0&q=:relevance-default-s&pageType=CATEGORY"
root_img = "https://www.amway.com"
next_page_obj = "data-target-page"

page = requests.get(root_url)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div", class_="amw-plp-item__content")

product_list = []

for a_result in results:
    try:
        product_name = a_result.find("h3", class_="amw-plp-item__name-wrapper")
        product_link = a_result.find("a", class_="amw-text amw-text--base amw-text--primary amw-text--semibold js-product-list-name")
        product_price = a_result.find("span",class_="amw-text amw-text--primary amw-text--base amw-text--semibold amw-text--nowrap")
        product_sku = a_result.find("span", class_="code js-plp-product-code")
        image_url = a_result.find("img", class_="amw-product-image__img js-lozad js-product-thumb-image js-image-cache")

        a_product = product()
        a_product.name = product_name.text.strip().replace("n* by Nutrilite™ ", "").encode('ascii', errors='ignore').decode()
        a_product.link = root_img + product_link["href"]
        a_product.price = product_price.text.strip()
        a_product.sku = product_sku.text
        a_product.img_url = root_img + image_url["data-src"]
        
        product_list.append(a_product)
    except Exception as e:
        print(e)
import csv

# open the file in the write mode
f = open('amway.csv', 'w')

for a_product in product_list:
    f.write(str(a_product))
f.close()

