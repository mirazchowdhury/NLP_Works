from selenium import webdriver
import time
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

driver.maximize_window()

# Open the product page
driver.get('https://www.daraz.com.bd/products/xt-02-s03-r1-i339044601-s1660491671.html?pvid=b0406b77-2cf8-4d58-88fe-bb6a177bafa0&search=jfy&scm=1007.51705.413671.0&spm=a2a0e.tm80335411.just4u.d_339044601')
driver.refresh()

# Scroll down to load the reviews section
height = driver.execute_script('return document.body.scrollHeight')
for i in range(0, height + 1000, 30):
    driver.execute_script(f'window.scrollTo(0,{i});')
    time.sleep(0.5)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div')))

reviews_data = {}  # Dictionary to store comments page-wise

# Loop through the first 10 pages of reviews
for i in range(1, 175):  
    page_comments = []  # List to store comments of each page
    
    try:
        # Identify the pagination button
        if i == 1:
            element = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div/button[1]')
        elif i == 2:
            element = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div/button[2]')
        elif i == 3:
            element = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div/button[3]')
        elif i >= 4 and i < 174:
            element = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div/button[4]')
        elif i == 174:
            element = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div/button[5]')
        else:
            element = driver.find_element(By.XPATH, f'/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div/button[{i}]')

        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)

        # Click using JavaScript to avoid interception
        driver.execute_script("arguments[0].click();", element)
        time.sleep(5)  # Wait for the page to load

        # Extract comments
        comments = driver.find_elements(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[2]/div')  # Adjust XPath if needed

        for comment in comments:
            page_comments.append(comment.text.strip())  # Store each comment

        reviews_data[f'page {i}'] = page_comments  # Store comments for current page

    except Exception as e:
        print(f"Error on page {i}: {e}")
        continue  # Continue to the next page even if there's an error

driver.quit()  # Close the browser

# Print the extracted comments
print(reviews_data)
