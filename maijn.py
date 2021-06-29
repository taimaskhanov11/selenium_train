import base64
import io

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

driver = webdriver.Chrome(
    executable_path="/home/rasul/PycharmProjects/selenium_train/googledriver/chromedriver",
    options=options
)

url = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&s=104&user=1'
url2 = 'https://www.avito.ru/moskva/kvartiry/1-k._kvartira_25m_22et._2190185057'
class_ = 'button item-phone-button js-item-phone-button button-origin contactBar_greenColor button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card contactBar_height'
class_2 = 'item-phone-button-sub-text'


def avito_auth(url):
    try:
        driver.get(url=url)

        driver.find_element_by_class_name('item-phone-button-sub-text').click()
        time.sleep(1)

        iframe2 = driver.find_element_by_xpath(
            "//div[@class='item-phone-number js-item-phone-number greenContact_color ']")
        photo = iframe2.find_element_by_xpath('//img').get_attribute('src')
        time.sleep(1)
        im = Image.open(io.BytesIO(base64.b64decode(photo.split(',')[1])))
        im.save("image.png")
        time.sleep(1)
    except Exception as exp:
        print(exp)

    finally:
        driver.close()
        driver.quit()


def main():
    avito_auth(url2)


if __name__ == '__main__':
    main()
