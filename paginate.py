from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def go_to_next_page(driver):
    time.sleep(2)
    # Check if the modal is present and close it
    try:
        modal = driver.find_element(By.CLASS_NAME, "actionBarMt0")
        if modal.is_displayed():
            modal_close_button = modal.find_element(By.TAG_NAME, "button")
            modal_close_button.click()

            time.sleep(1)  # Give some time for the modal to close
    except:
        pass

    # Click on the "Next" button
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-test='pagination-next']")
            )
        )
        next_button.click()
    except Exception as e:
        print(
            "modal found when trying to click the button"
            if modal.is_displayed
            else "no modal found when trying to click the next button"
        )
        print("Error trying to click the next page button", repr(e))


def next_page_found(driver):
    time.sleep(4)
    try:
        modal = driver.find_element(By.CLASS_NAME, "actionBarMt0")

        if modal.is_displayed():
            modal_close_button = modal.find_element(By.TAG_NAME, "button")
            modal_close_button.click()

    except Exception as e:
        print("modal not found")

    try:
        next_button = driver.find_elements(
            By.CSS_SELECTOR, "button[data-test='pagination-next']"
        )

        if next_button:
            return True
        else:
            return False

    except Exception as e:
        print("error:", repr(e))
        # return False
