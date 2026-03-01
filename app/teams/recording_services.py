from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def enable_auto_recording(driver, url: str, auto_record: bool):
    print(f"Processing URL: {url}")
    driver.get(url)

    checkbox_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "AutoRecordingEnabled"))
    )

    label = checkbox_input.find_element(By.XPATH, "./..")
    is_checked = checkbox_input.get_attribute("aria-checked")

    # Convert string to boolean
    currently_enabled = is_checked == "true"

    print(f"Current state: {'ON' if currently_enabled else 'OFF'}")
    print(f"Desired state: {'ON' if auto_record else 'OFF'}")

    # Only change if needed
    if currently_enabled != auto_record:
        label.click()

        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@aria-label="Save"]')
            )
        )
        save_button.click()

        print("Auto recording set to " + ("ON." if auto_record else "OFF."))
        time.sleep(2)

    else:
        print("No change needed.")