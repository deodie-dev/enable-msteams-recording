from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# def create_driver(chromedriver_path: str):
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")

#     return webdriver.Chrome(
#         service=Service(chromedriver_path),
#         options=options
#     )

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)