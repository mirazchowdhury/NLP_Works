#products per pagination link extract

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
#driver.get("https://www.daraz.com.bd/routers/")
driver.maximize_window()
link_list = []

for page_no in range(1,10):
    driver.get(f'https://www.daraz.com.bd/routers/?page={page_no}')
    driver.maximize_window()
    for product in range(1,21):
        type_product = str(product)
        link = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div['+type_product+']/div/div/div[2]/div[2]/a').get_attribute('href')
        link_list.append(link)
print(link_list)
print(len(link_list))