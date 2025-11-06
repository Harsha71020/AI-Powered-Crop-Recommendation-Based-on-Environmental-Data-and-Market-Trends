from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import pytest, time, os, datetime

BASE_URL = "http://127.0.0.1:5000/"

# ---------------- Helper functions ---------------- #

def wait_for(driver, element_id, timeout=15):
    """Wait until an element with given ID is visible."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )

def take_screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    filename = f"screenshots/{name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    driver.save_screenshot(filename)

@pytest.fixture
def driver():
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run quietly without opening a window
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# ---------------- Actual Tests ---------------- #

def test_valid_login(driver):
    driver.get(BASE_URL)
    wait_for(driver, "username").send_keys("valid_user")
    wait_for(driver, "password").send_keys("valid_pass")
    wait_for(driver, "loginButton").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    print("[PASS] Valid login test passed")

def test_invalid_login(driver):
    driver.get(BASE_URL)
    wait_for(driver, "username").send_keys("invalid_user")
    wait_for(driver, "password").send_keys("wrong_pass")
    wait_for(driver, "loginButton").click()
    msg = wait_for(driver, "errorMsg").text
    assert "invalid" in msg.lower()
    print("[PASS] Invalid login test passed")

def test_empty_fields(driver):
    driver.get(BASE_URL)
    wait_for(driver, "loginButton").click()

    msg_text = ""
    for _ in range(5):
        try:
            msg_el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "validationMsg"))
            )
            msg_text = msg_el.text.strip()
            if msg_text:
                break
        except (StaleElementReferenceException, TimeoutException):
            time.sleep(0.3)
            continue

    assert "required" in msg_text.lower()
    print("[PASS] Empty fields test passed")
