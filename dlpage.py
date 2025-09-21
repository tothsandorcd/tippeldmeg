from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import sys

# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Formatter with milliseconds
formatter = logging.Formatter(
   '%(asctime)s.%(msecs)03d - %(message)s',  # add milliseconds separately
   datefmt='%Y-%m-%d %H:%M:%S'
)

# Handler for stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Handler for file
file_handler = logging.FileHandler('dlpage.log')
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("Download script started")

# Configure Chrome to run headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # No GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")  # Explicit path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)
logger.info("webdriver started")

# Open login page
driver.get("https://tippeldmeg.hu/")

# Fill login form
driver.find_element(By.NAME, "email").send_keys("tothsandorcc@gmail.com")
driver.find_element(By.NAME, "password").send_keys("Gevinet1" + Keys.RETURN)

# Wait for login to complete
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "details_3891")))
logger.info("logged in")

# 4. Click all chevron elements to expand details
chevrons = driver.find_elements(By.CSS_SELECTOR, "i.fa.fa-chevron-down")
print(f"Found {len(chevrons)} elements to expand.")

i = 1
count = len(chevrons)

for chevron in chevrons:
    if i % 10 == 0 or i == count or i == 1:
        print(f"Processing {i}/{count}...")
    i += 1
    
    try:
        driver.execute_script("arguments[0].click();", chevron)
        time.sleep(0.2)  # Small delay to allow content to expand
    except Exception as e:
        print(f"Failed to click an element: {e}")

# Wait for all content to be fully visible
time.sleep(3)

# 5. Save the fully expanded HTML
html = driver.page_source
with open("page_actual.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()
print("HTML saved to page_actual.html")
