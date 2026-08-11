from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def enable_auto_recording(driver, url: str, auto_record: bool):
    print(f"Processing URL: {url}")
    driver.get(url)

    try:
        dropdown = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "AutoRecordAndTranscribeMode"))
        )

        current_value = dropdown.get_attribute("value")

        print(f"Current value: {current_value}")
        print("Desired value: Record and transcribe")

        if current_value != "Record and transcribe":

            dropdown.click()

            option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[text()="Record and transcribe"]'
                ))
            )

            option.click()

            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@aria-label="Save"]')
                )
            )

            save_button.click()

            print("Auto recording set to 'Record and transcribe'.")
            time.sleep(2)

        else:
            print("No change needed.")

    except Exception as e:
        # print(f"Error enabling auto recording: {e}")
        print("Unable to update auto recording. It might already be set or the meeting might not support this feature. Pleae check the meeting settings manually.")






















    # dropdown = WebDriverWait(driver, 30).until(
    #     EC.element_to_be_clickable((By.ID, "AutoRecordAndTranscribeMode"))
    # )

    # current_value = dropdown.get_attribute("value")

    # print(f"Current value: {current_value}")
    # print("Desired value: Record and transcribe")

    # if current_value != "Record and transcribe":

    #     dropdown.click()

    #     option = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((
    #             By.XPATH,
    #             '//*[text()="Record and transcribe"]'
    #         ))
    #     )

    #     option.click()

    #     save_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable(
    #             (By.XPATH, '//button[@aria-label="Save"]')
    #         )
    #     )

    #     save_button.click()

    #     print("Auto recording set to 'Record and transcribe'.")
    #     time.sleep(2)

    # else:
    #     print("No change needed.")