#extracting links form a webpage 

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get("https://www.daraz.com.bd/routers/")
link = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/a')
print(link)
driver.get(link.get_attribute('href'))
print(link.get_attribute('href'))
time.sleep(1000)
driver.quit()
