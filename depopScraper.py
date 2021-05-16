from bs4 import BeautifulSoup
from selenium import webdriver
import time

# url of the page we want to scrape
from selenium.webdriver.common.keys import Keys

home = input("Enter URL:")

driver = webdriver.Chrome('./chromedriver')
driver.get(home)
# ensure the page loads image source (dynamic property)
time.sleep(3)

elem = driver.find_element_by_tag_name("body")

no_of_pagedowns = 20

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

urls = soup.find_all("a", {"data-testid" : "product__item"})


def scrape_data(url):
    # Open the chrome web driver
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    # ensure the page loads image source (dynamic property)
    time.sleep(1)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    descriptionHtml = soup.find(class_="Text-yok90d-0 styles__DescriptionContainer-uwktmu-9 bWcgji")

    desc = descriptionHtml.contents[0]

    priceHtml = soup.find("span", {"data-testid" : "fullPrice"})

    price = priceHtml.contents[0]

    img = soup.find("img", {"class" : "styles__Image-uwktmu-7 cKdjfY LazyLoadImage__Image-sc-1732jps-1 cSwkPp"})

    src = img.get("src")

    # close the web driver
    driver.close()

    return "INSERT INTO products VALUES ('" + price + "', '" + src + "', '" + desc + "');"


print("CREATE TABLE products (price int, src varchar(255), descr varchar(255)); ")

for i in urls:
    print(scrape_data("https://www.depop.com" + i.get("href")))

driver.close()
