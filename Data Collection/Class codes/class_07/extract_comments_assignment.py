from selenium import webdriver
import time
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

driver.maximize_window()

driver.get('https://www.daraz.com.bd/products/hoco-hc2-wireless-bluetooth-speaker-i350816250-s2242226639.html?pvid=0a5f0b3b-0df0-4962-8690-6a4a6f566314&search=jfy&scm=1007.51705.413671.0&spm=a2a0e.tm80335411.just4u.d_350816250')
driver.refresh()

# Scroll to load the reviews section
height = driver.execute_script('return document.body.scrollHeight')
for i in range(0, height+1000, 30):
    driver.execute_script(f'window.scrollTo(0,{i});')
    time.sleep(0.5)

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div')))

reviews_data = {}  # Dictionary to store comments page-wise

for i in range(1, 10):  
    page_comments = []  # List to store comments of each page
    
    #Identify the pagination button
    if i == 1:
        element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[1]')
    elif i == 2:
        element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[2]')
    elif i == 3:
        element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[3]')
    elif i >= 4 and i < 9:
        element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[4]')
    elif i == 9:
        element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[5]')
    else:
        element = driver.find_element(By.XPATH, f'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[{i}]')

    element.click()


    # if(i>=4 and i<5):
    #     j='4'
    #     #print(4)
    #     element = driver.find_element(By.XPATH, f'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[{j}]')
    #     #loop_list.append(4)
    # elif(i==5):
    #     element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[5]')
    #     #loop_list.append(5)
    # else:
    #     element = driver.find_element(By.XPATH, f'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[{i}]')
    #     #print(i)
    #     #loop_list.append(i)
    # element.click()
    # time.sleep(5)  # Wait for page to load

    
    # Extract comments
    comments = driver.find_elements(By.XPATH, '//*[@id="module_product_review"]/div/div/div[2]/div')  # Adjust the XPath according to website

    for comment in comments:
        page_comments.append(comment.text.strip())  # Store each comment

    reviews_data[f'page {i}'] = page_comments  # Store comments for current page

driver.quit()  # Close the browser

# Print the extracted comments
print(reviews_data)
