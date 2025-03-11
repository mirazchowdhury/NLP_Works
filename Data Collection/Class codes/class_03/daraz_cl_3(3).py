from selenium import webdriver
import time
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get("https://www.daraz.com.bd/routers/?page=1")
driver.maximize_window()
total_number_page = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div/div/span[1]').text
total_number_page = int(total_number_page.split()[0])
print(f'total : {total_number_page}')
