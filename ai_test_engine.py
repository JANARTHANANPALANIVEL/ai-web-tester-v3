import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import json
import time
import base64
from config import Config

# Configure Gemini API
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
    
    # Use your ChromeDriver path
    driver = webdriver.Chrome(
        executable_path=Config.SELENIUM_DRIVER_PATH,
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
        # Run Lighthouse CLI and save the report to a JSON file
        report_file = "lighthouse_report.json"
        subprocess.run(
            f"lighthouse {url} --output=json --output-path={report_file} --quiet --chrome-flags='--headless=new'",
            shell=True,
            check=True
        )
        
        # Read and parse the JSON report
        with open(report_file, "r") as f:
            report_data = json.load(f)
        
        return report_data
    except subprocess.CalledProcessError as e:
        return {"error": f"Lighthouse failed with exit code {e.returncode}"}
    except Exception as e:
        return {"error": str(e)}

def run_security_test(url):
    try:
        # Use your ZAP path
        result = subprocess.check_output(
            f'"{Config.ZAP_PATH}" -cmd -quickurl {url} -quickprogress -quickout report.json',
            shell=True
        )
        with open("report.json", "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def run_full_audit(url):
    return {
        "functional": run_selenium_test(url),
        "performance": run_performance_test(url),
        "security": run_security_test(url)
    }