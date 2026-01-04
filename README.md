AutoResultX is a Python-based automation tool that extracts university results from a JavaScript-rendered, SSL-restricted portal using Selenium and exports them to Excel.

It is designed to handle dynamic content, SSL warnings, and browser automation challenges commonly found in real-world academic portals.

 Features:

 Automatic roll number generation

 Supports adding extra/custom roll numbers

 Handles JavaScript-rendered (SPA) websites

 Bypasses SSL “Your connection is not private” warnings

 Reuses a single browser session (optimized performance)

 Extracts SGPA and Result (PASS/FAIL)

 Exports results to Excel (.xlsx)

 Clean, modular Python project structure

Tech Stack:
Python 3
Selenium
Pandas
OpenPyXL
Brave Browser (Chromium-based)

📁 Project Structure
AutoResultX/
│
├── main.py               # Main controller script
├── selenium_fetcher.py   # Selenium automation logic
├── roll_generator.py     # Roll number generation
├── save_excel.py         # Excel export logic
│
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignored files
├── LICENSE               # MIT License
└── README.md             # Project documentation

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/siddharthakuchana/AutoResultX.git
cd AutoResultX

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Install ChromeDriver

Download ChromeDriver matching your Brave/Chrome version

Place chromedriver.exe in your system or project path

Do not upload it to GitHub

4️⃣ Configure paths (if needed)

In main.py, update:

CHROMEDRIVER_PATH = "path/to/chromedriver.exe"
BRAVE_PATH = "path/to/brave.exe"

▶️ How to Run
python main.py


Browser opens once

Results are fetched sequentially

Output is saved as results.xlsx

📊 Output Example
Roll Number	SGPA	Result
23011A6601	7.60	PASS
23011A6602	8.12	PASS
22011A6659	6.95	PASS
🧠 Key Learnings & Challenges Solved

Handling SSL-blocked websites in browser automation

Working with React/SPA-based DOM rendering

Debugging invisible inputs and JS-driven events

Optimizing Selenium to reuse a single browser instance

Writing production-style Python automation code

⚠️ Important Notes

This project is intended for educational and personal use

Do not overload servers with excessive requests

ChromeDriver and output files are intentionally ignored via .gitignore

📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it with attribution.

👤 Author

Siddharth Kuchana
GitHub: siddharthakuchana

🌟 Future Improvements

Flask-based web interface

Headless browser support

Progress bar & logging

Multi-semester support

