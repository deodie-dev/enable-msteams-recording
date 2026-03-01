from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login_microsoft(driver, email: str, password: str):
    driver.get("https://login.microsoftonline.com")

    wait = WebDriverWait(driver, 20)
    email_input = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
    email_input.send_keys(email)
    wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    time.sleep(2)

    password_input = wait.until(EC.presence_of_element_located((By.ID, "i0118")))
    password_input.send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    time.sleep(2)

    try:
        wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    except:
        pass

    print("Successfully signed in.")