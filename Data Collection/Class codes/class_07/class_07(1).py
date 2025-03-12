from selenium import webdriver
import time
from selenium.webdriver.common.by import By  # Corrected import statement
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()

driver.maximize_window()

driver.get('https://www.daraz.com.bd/products/oraimo-enc-otw-330-i367303135-s1937479009.html?scm=1007.51610.379274.0&pvid=8f9ca975-f5af-42c5-a22a-1522d1348e0b&search=flashsale&spm=a2a0e.tm80335411.FlashSale.d_367303135')
driver.refresh()

# to execute javascript code on python, we need to use driver.execute_script()
height = driver.execute_script('return document.body.scrollHeight') 
print(height)

for i in range(0,height+1000,30):
    driver.execute_script(f'window.scrollTo(0,{i});')
    time.sleep(0.5)

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div')))

loop_list = []
#global element

for i in range(1, 11):  
    if i == 1:
        element = driver.find_element(By.XPATH,'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[1]')
        #loop_list.append(1)  
    elif i == 2:
        element = driver.find_element(By.XPATH,'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[2]')   
        #loop_list.append(i)  
    elif i == 3:
        element = driver.find_element(By.XPATH,'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[3]')  
        #loop_list.append(i)  
    elif i >= 4 and i < 10:
        element = driver.find_element(By.XPATH,'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[4]')
        #loop_list.append(4)  
    elif i == 10:
        element = driver.find_element(By.XPATH,'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[5]')  
        #loop_list.append(5)  
    else:
        element = driver.find_element(By.XPATH,f'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[{i}]')  
        #loop_list.append(i)
    element.click()
    time.sleep(5)  