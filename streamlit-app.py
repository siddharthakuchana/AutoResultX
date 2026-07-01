import time
import pandas as pd
import streamlit as st
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- HELPER FUNCTIONS ---

def generate_roll_numbers(base_roll, start, end, extra_rolls_str):
    """Generates a sorted, unique list of roll numbers."""
    rolls = [base_roll + str(i).zfill(2) for i in range(start, end + 1)]
    if extra_rolls_str:
        # Split by comma and strip whitespaces
        extra_rolls = [r.strip() for r in extra_rolls_str.split(",") if r.strip()]
        rolls.extend(extra_rolls)
    return sorted(set(rolls))

def get_headless_driver():
    """Initializes a headless Selenium driver compatible with server deployments."""
    options = Options()
    options.add_argument("--headless=new")  # Critical for cloud deployment
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Automatically manages the driver binary without local paths
    service = Service(ChromeDriverManager().search())
    return webdriver.Chrome(service=service, options=options)

def fetch_result(driver, roll_number):
    """Fetches SGPA and Result for a given roll number."""
    try:
        driver.refresh()
        time.sleep(4)  # Reduced slightly to optimize, adjust if server is slow

        # Send roll number at page level
        body = driver.switch_to.active_element
        body.send_keys(roll_number)
        body.send_keys(Keys.ENTER)

        time.sleep(5)  # Wait for results DOM to update

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
            raise Exception("DOM data returned empty")

        return {
            "Roll Number": roll_number,
            "SGPA": data["sgpa"],
            "Result": data["result"]
        }

    except Exception as e:
        return {
            "Roll Number": roll_number,
            "SGPA": "Error/Not Found",
            "Result": f"Error: {str(e)}"
        }

# --- STREAMLIT UI ---

st.set_page_config(page_title="JNTUH Result Scraper", page_icon="📊", layout="centered")

st.title("📊 Automated Result Fetcher")
st.write("Enter the results portal URL and target range to scrape data into an Excel spreadsheet.")

# Input fields
results_url = st.text_input("Result Portal URL", placeholder="https://results.jntuhceh.ac.in/result/...")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    base_roll = st.text_input("Base Roll Number Prefix", value="23011A66")
with col2:
    start_num = st.number_input("Start Index", min_value=1, max_value=999, value=1)
with col3:
    end_num = st.number_input("End Index", min_value=1, max_value=999, value=78)

extra_rolls_input = st.text_input("Extra Roll Numbers (comma-separated if any)", placeholder="22011A6659, 23011A6680")

# Execution block
if st.button("🚀 Generate and Fetch Results", type="primary"):
    if not results_url:
        st.error("Please enter a valid Result Portal URL.")
    else:
        roll_numbers = generate_roll_numbers(base_roll, start_num, end_num, extra_rolls_input)
        
        st.info(f"Total roll numbers to process: {len(roll_numbers)}")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        
        # Initialize browser in background
        status_text.text("Initializing headless browser instance...")
        try:
            driver = get_headless_driver()
            driver.get(results_url)
            time.sleep(5)  # Initial load
            
            # Processing Loop
            for index, roll in enumerate(roll_numbers):
                status_text.text(f"Fetching data for: {roll} ({index + 1}/{len(roll_numbers)})")
                data = fetch_result(driver, roll)
                results.append(data)
                
                # Update progress bar
                progress_bar.progress((index + 1) / len(roll_numbers))
            
            driver.quit()
            status_text.text("Scraping completed! Compiling data...")
            
            # Convert to DataFrame
            df = pd.DataFrame(results)
            
            # Show a sample preview in the browser
            st.subheader("📋 Results Preview")
            st.dataframe(df)
            
            # Generate memory-based Excel download button (doesn't leave file clutter on the server)
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Results')
            
            st.download_button(
                label="📥 Download Results as Excel",
                data=buffer.getvalue(),
                file_name="jntuh_scraped_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        except Exception as global_err:
            st.error(f"A critical error occurred: {global_err}")
            if 'driver' in locals():
                driver.quit()
