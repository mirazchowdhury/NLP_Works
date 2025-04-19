import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor #This lets us run multiple browser sessions at the same time using threads (for multithreading).
import time
import logging #Used for logging errors into a file.

# ------------------ CONFIG ------------------
EXCEL_FILE = "form_data.xlsx"
#FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScXMBYpXNUL__dS7qanUQNGVWyEO-2mAd8sVCc4uuCIG08bSg/viewform?usp=dialog"
#CHROMEDRIVER_PATH = "G:\chromedriver-win64\chromedriver.exe"
 # ✅ Use raw string or double backslashes
MAX_WORKERS = 10  # Number of parallel threads
TEST_BATCH_SIZE = 2  # Start small for testing

#MAX_WORKERS: Number of browser instances (threads) running in parallel.

#TEST_BATCH_SIZE: Number of rows to test from the Excel file (small batch to test things before doing all 1 lakh).

# --------------------------------------------

# Logging setup
logging.basicConfig(filename='form_errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

#This line sets up error logging:
#All errors will be written in form_errors.log
#It will include a timestamp.

# Load Excel data
df = pd.read_excel(EXCEL_FILE)
data_list = df.to_dict(orient="records") #.to_dict(orient="records") converts it into a list of dictionaries, where each dictionary is one form entry.


def fill_form(entry):
    """Fills and submits a Google Form with one entry."""
    options = Options()
    #options.add_argument("--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data")
    #options.add_argument("--profile-directory=Default") 
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito") 

    driver = webdriver.Chrome() #executable_path=CHROMEDRIVER_PATH, options=options
    

    try:
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLScXMBYpXNUL__dS7qanUQNGVWyEO-2mAd8sVCc4uuCIG08bSg/viewform?usp=dialog")
        driver.maximize_window()
        time.sleep(200)  # Let the page load

        # Update XPaths or aria-labels as per your Google Form fields
        driver.find_element(By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP').send_keys(entry["Name"])
        driver.find_element(By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(2) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP').send_keys(entry["Email"])
        driver.find_element(By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(3) > div > div > div.AgroKb > div > div.RpC4Ne.oJeWuf > div.Pc9Gce.Wic03c').send_keys(str(entry["Address"]))
        driver.find_element(By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(4) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP').send_keys(str(entry["Phone number"]))
        driver.find_element(By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(5) > div > div > div.AgroKb > div > div.RpC4Ne.oJeWuf > div.Pc9Gce.Wic03c').send_keys(entry["Comments"])

        # Submit button
        driver.find_element(By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > div.lRwqcd > div > div.e19J0b.CeoRYc').click()
        time.sleep(5)

        print(f"Submitted: {entry['Email']}")

    except Exception as e:
        logging.error(f"Failed entry: {entry} | Error: {e}")
    finally:
        driver.quit()
    #If something goes wrong, it logs the error.

    #Always closes the browser window (important to free memory).


def run_batch(entries, workers=MAX_WORKERS):
    """Runs form submissions in parallel and returns time taken."""
    start = time.time()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(fill_form, entries)

    end = time.time()
    return end - start


if __name__ == "__main__":
    print(f"Starting test run with {TEST_BATCH_SIZE} entries and {MAX_WORKERS} threads...")

    test_entries = data_list[:TEST_BATCH_SIZE]  # Use a smaller batch first
    elapsed = run_batch(test_entries)

    print(f"Time taken for {TEST_BATCH_SIZE} entries: {elapsed:.2f} seconds")

    estimated_time = (elapsed / TEST_BATCH_SIZE) * 100000
    print(f"Estimated time for 1 lakh entries: {estimated_time / 60:.2f} minutes")
