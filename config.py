import os

class Config:
    # Set your Gemini API key
    GEMINI_API_KEY = "AIzaSyB-P3HZMwMsfafxmC2dFIBamTYjkVfGXmA"
    
    # Set your ChromeDriver path
    SELENIUM_DRIVER_PATH = r"J:/chromedriver/chromedriver.exe"
    
    # Set your ZAP path
    ZAP_PATH = r"C:/Program Files/ZAP/Zed Attack Proxy/zap-2.16.0.jar"
    # Other configurations
    ALLURE_DIR = "reports"
    WAIT_TIMEOUT = 10
    HEADLESS = False  # Set to True if you want to run in headless mode
    