import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import json
import time
import base64
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_selenium_code(url):
    response = genai.generate_text(
        model="models/text-bison-001",
        prompt=f"""Generate Python Selenium test code for {url} including:
        - WebDriverWait with EC conditions
        - CSS selectors preferred
        - Page object pattern
        - At least 3 meaningful tests
        - Try/except blocks for error handling
        - Screenshot on failure""",
        temperature=0.7
    )
    return response.result

def run_selenium_test(url):
    options = webdriver.ChromeOptions()
    if Config.HEADLESS:
        options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(),
        options=options
    )
    wait = WebDriverWait(driver, Config.WAIT_TIMEOUT)
    
    try:
        test_code = generate_selenium_code(url)
        exec_globals = {
            'driver': driver,
            'By': By,
            'EC': EC,
            'wait': wait,
            'url': url
        }
        exec(test_code, exec_globals)
        return {"status": "passed", "output": test_code}
    except Exception as e:
        screenshot = base64.b64encode(driver.get_screenshot_as_png()).decode('utf-8')
        return {"status": "failed", "error": str(e), "screenshot": screenshot}
    finally:
        driver.quit()

def run_performance_test(url):
    try:
        result = subprocess.check_output(
            f"lighthouse {url} --output=json --quiet --chrome-flags='--headless=new'",
            shell=True
        )
        return json.loads(result)
    except Exception as e:
        return {"error": str(e)}

def run_security_test(url):
    try:
        result = subprocess.check_output(
            f"docker run --rm -v $(pwd):/zap/wrk/ owasp/zap2docker-stable zap-baseline.py "
            f"-t {url} -J report.json",
            shell=True
        )
        return json.loads(result)
    except Exception as e:
        return {"error": str(e)}

def run_full_audit(url):
    return {
        "functional": run_selenium_test(url),
        "performance": run_performance_test(url),
        "security": run_security_test(url)
    }