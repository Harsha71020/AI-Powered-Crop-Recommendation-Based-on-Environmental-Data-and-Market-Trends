import os
from datetime import datetime

def take_screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"[Screenshot saved]: {filename}")
