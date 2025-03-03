import os

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB-P3HZMwMsfafxmC2dFIBamTYjkVfGXmA")
    SELENIUM_DRIVER_PATH = os.getenv("SELENIUM_DRIVER_PATH", "J:\chromedriver\chromedriver.exe")
    ALLURE_DIR = "reports"
    WAIT_TIMEOUT = 10
    HEADLESS = False