from selenium.webdriver.common.keys import Keys
import time

def fetch_result(driver, roll_number):
    """
    Fetch SGPA and Result for a given roll number
    using an already-open Selenium driver.
    """

    try:
        # Refresh page to reset state
        driver.refresh()
        time.sleep(6)

        # Send roll number at page level
        body = driver.switch_to.active_element
        body.send_keys(roll_number)
        body.send_keys(Keys.ENTER)

        # Wait for result to load
        time.sleep(8)

        # Extract SGPA & Result from DOM
        data = driver.execute_script("""
            const cells = document.querySelectorAll('[data-title]');
            let sgpa = null;
            let result = null;

            cells.forEach(c => {
                const title = c.getAttribute('data-title');
                if (!title) return;

                const t = title.toUpperCase();
                if (t.includes('SGPA')) sgpa = c.innerText.trim();
                if (t.includes('RESULT')) result = c.innerText.trim();
            });

            return { sgpa: sgpa, result: result };
        """)

        if not data["sgpa"] or not data["result"]:
            raise Exception("SGPA or Result not loaded")

        return {
            "Roll Number": roll_number,
            "SGPA": data["sgpa"],
            "Result": data["result"]
        }

    except Exception as e:
        print("ERROR for", roll_number, "->", e)
        return {
            "Roll Number": roll_number,
            "SGPA": "Error",
            "Result": "Error"
        }
