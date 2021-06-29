import base64
import io
import os
from datetime import datetime

import requests
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# options
# options = webdriver.ChromeOptions()
#
# # user-agent
# options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
# options.add_argument('headless')
# driver = webdriver.Chrome(
#     executable_path="/home/rasul/PycharmProjects/selenium_train/googledriver/chromedriver",
#     options=options
# )

site = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&s=104&user=1'

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)




def avito_auth(url):
    try:
        driver.get(url=url)
        # soup = BeautifulSoup(res, 'lxml')
        #
        time.sleep(1)
        all_ads = driver.find_element_by_class_name('items-items-38oUm')
        one_ads = all_ads.find_element_by_class_name('iva-item-content-m2FiN')

        url_ad = one_ads.find_element_by_tag_name('a').get_attribute('href')  # !урл обьявления
        #
        driver.get(url=url_ad)
        #
        time.sleep(1)#todo
        price_ad = driver.find_element_by_class_name('item-price-wrapper').text  # !цена
        name_user_ad = driver.find_element_by_class_name('seller-info-value').find_element_by_tag_name(
            'a').get_attribute('text').strip()  # ! имя

        address_ad = driver.find_element_by_class_name('item-address__string').text.strip()  # !адрес
        name_ad = driver.find_element_by_class_name('title-info-title-text').text.strip()  # !название
        time_ad = driver.find_element_by_class_name('title-info-metadata-item-redesign').text.strip()
        # # атрибутный состав: название, метро, цена, адрес, имя, телефон, урл обьявления
        return ({'text': f"Название - {name_ad}\n"
                         f"Цена - {price_ad} ₽ в месяц\n"
                         f"Адрес - {address_ad}\n"
                         f"Имя - {name_user_ad}\n"
                         f"Телефон ...\n"
                         f"URL Объявления - {url_ad} \n"
                         f"Время объявления {time_ad}", 'time': time_ad})

    except Exception as exp:
        print(exp)

    finally:
        driver.close()
        driver.quit()

def correct_time(string):
    print(string)
    c = string[-1:-6:-1]
    # b = time.strptime(c[::-1], '%H:%M')
    b = datetime.strptime(c[::-1], '%H:%M')
    return b


def main():
    print(avito_auth(site))


if __name__ == '__main__':
    main()
