import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome driver options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1080,720")
chrome_options.add_argument("--no-sandbox")

# Set path to your Chrome driver executable
webdriver_path = "/path/to/chromedriver"

# Instantiate Chrome driver
driver = webdriver.Chrome(
    service=Service(executable_path=webdriver_path), options=chrome_options
)

# Open Glassdoor website
driver.get("https://www.glassdoor.com/index.htm")

# Find and interact with the sign-in link
signin_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#inlineUserEmail"))
)
signin_link.click()

time.sleep(2)

# Find and interact with the email input field
# email_input = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "username"))
# )
signin_link.send_keys("your_email@example.com")  # Replace with your email
time.sleep(2)

print("hi")

# Find and interact with the password input field
# password_input = driver.find_element(By.ID, "userPassword")
# password_input.send_keys("your_password")  # Replace with your password

# Find and interact with the sign-in button
# signin_button = driver.find_element(By.CSS_SELECTOR, ".gd-ui-button[type='submit']")
# signin_button.click()

# # Wait for the sign-in process to complete
# time.sleep(5)  # Adjust as needed

# # Find and interact with the search input field
# search_input = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "sc.keyword"))
# )
# search_input.send_keys("Your keyword")  # Replace with your desired keyword
# search_input.send_keys(Keys.RETURN)

# # Wait for the search results to load
# WebDriverWait(driver, 10).until(EC.title_contains("Search Results"))

# # Get the URL of the search results page
# search_results_url = driver.current_url
# print("Search Results URL:", search_results_url)

# Close the browser
# driver.quit()
