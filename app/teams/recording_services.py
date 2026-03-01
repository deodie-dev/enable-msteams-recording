from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def enable_auto_recording(driver, url: str):
    print(f"Processing URL: {url}")
    driver.get(url)

    checkbox_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "AutoRecordingEnabled"))
    )

    label = checkbox_input.find_element(By.XPATH, "./..")
    is_checked = checkbox_input.get_attribute("aria-checked")

    if is_checked == "false":
        label.click()

        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@aria-label="Save"]')
            )
        )
        save_button.click()
        print("Auto recording enabled.")
        time.sleep(2)
    else:
        print("Already enabled.")