from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from roll_generator import generate_roll_numbers
from selenium_fetcher import fetch_result
from save_excel import save_to_excel

# ---------------- CONFIG ----------------
BASE_ROLL = "23011A66"
START = 1
END = 78
EXTRA_ROLLS = ["22011A6659"]

RESULTS_URL = "https://results.jntuhceh.ac.in/result/0970ac0c3347fb3b3e68fcea7e49896a"
CHROMEDRIVER_PATH = r"C:\Users\r̥ṭñ\Desktop\python projects\chromedriver.exe"
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# ----------------------------------------

# Generate roll numbers
roll_numbers = generate_roll_numbers(BASE_ROLL, START, END)
roll_numbers.extend(EXTRA_ROLLS)
roll_numbers = sorted(set(roll_numbers))

results = []

# ✅ OPEN BROWSER ONCE
options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

driver.get(RESULTS_URL)
import time
time.sleep(8)

try:
    for roll in roll_numbers:
        print(f"Fetching result for {roll}")
        data = fetch_result(driver, roll)
        results.append(data)

finally:
    # ✅ CLOSE BROWSER ONCE
    driver.quit()

save_to_excel(results)
print("DONE! Results saved to results.xlsx")
