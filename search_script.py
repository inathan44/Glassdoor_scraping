import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Enable logging
logging.basicConfig(level=logging.INFO)

# Set up Chrome driver options
chrome_options = Options()
# Commenting out headless mode for troubleshooting
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1080,720")
chrome_options.add_argument("--no-sandbox")

# Set path to your Chrome driver executable
webdriver_path = "/path/to/chromedriver"

# Instantiate Chrome driver
driver = webdriver.Chrome(
    service=Service(executable_path=webdriver_path), options=chrome_options
)

try:
    # Open Glassdoor website
    driver.get("https://www.glassdoor.com/index.htm")

    # Find and interact with the search input field
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sc.keyword"))
    )
    search_input.send_keys("Your keyword")  # Replace with your desired keyword
    search_input.send_keys(Keys.RETURN)

    # Wait for the search results to load
    WebDriverWait(driver, 10).until(EC.title_contains("Search Results"))

    # Get the URL of the search results page
    search_results_url = driver.current_url
    print("Search Results URL:", search_results_url)

except Exception as e:
    print("An exception occurred:", str(e))

finally:
    # Close the browser
    driver.quit()
