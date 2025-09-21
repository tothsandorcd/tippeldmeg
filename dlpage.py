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

rows = driver.find_elements(By.CSS_SELECTOR, "div.row")
logger.info(f"Found {len(rows)} rows to inspect.")

i = 1
skipped = 0

for row in rows:
    # Check if there’s a matchdetail link inside this row
    links = row.find_elements(By.CSS_SELECTOR, 'a[href*="matchdetail"]')
    if not links:
        continue  # Skip rows without matchdetail links

    # Find chevron inside the same row
    chevrons = row.find_elements(By.CSS_SELECTOR, "i.fa.fa-chevron-down, i.fa.fa-chevron-up")
    if not chevrons:
        skipped += 1
        continue

    chevron = chevrons[0]  # take first chevron in that row

    logger.info(f"Clicking chevron {i} in row containing matchdetail link...")
    i += 1

    try:
        driver.execute_script("arguments[0].click();", chevron)
        time.sleep(0.2)  # allow content to expand
    except Exception as e:
        logger.info(f"Failed to click chevron in row: {e}")

logger.info(f"Not yet played matches: {skipped}")

# Wait for all content to be fully visible
logger.info("Waiting 3 sec for content ready")
time.sleep(3)

# 5. Save the fully expanded HTML
html = driver.page_source
with open("page_actual.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()
print("HTML saved to page_actual.html")
