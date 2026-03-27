Twitter (X) Stealth Scraper Suite
A collection of Python scripts designed to extract real-time and historical data from Twitter (X) using Selenium Remote Debugging. By connecting to an existing browser session, these tools bypass the need for automated login flows, significantly reducing the risk of account suspension.

Key Features
Remote Debugging Connection: Connects to an active Chrome window (port 9222). This allows you to log in manually and let the script take over the authenticated session.
Safe Scrape Logic: Implements randomized scrolling, human-like wait times, and URL encoding to mimic organic search behavior.
Two Specialized Modes:
Live Scraper (twitter_baglan.py): Focuses on the most recent/live tweets for a set of keywords.
Historical Date Hunter (twitter_date_avı.py): Uses advanced search operators (since and until) to pull data from a specific past timeframe (e.g., the last 30 days).
Duplicate Prevention: Uses Python sets to ensure that even if the page refreshes or scrolls back, each tweet is only recorded once.
Excel Reporting: Automatically exports results to .xlsx with columns for Keyword, Date/Time, and Tweet Content.

Setup (Crucial)
Unlike standard Selenium scripts, you must launch Chrome in debug mode first:
Close all Chrome windows.
Open Terminal/CMD and run:
Bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"
Log in to Twitter in that specific window.

Install dependencies:
Bash
pip install selenium webdriver-manager pandas openpyxl
📖 Usage
1. General Live Scraping
Run twitter_baglan.py to get the latest mentions of your brands or competitors.

Bash
python twitter_baglan.py
2. Time-Travel Scraping
Run twitter_date_avı.py to collect data from a specific window of time. You can adjust the gun_sayisi (day count) variable in the code.

Bash
python twitter_date_avı.py

Technical Details
URL Encoding: Uses urllib.parse.quote to handle special characters and hashtags in search queries.
Anti-Detection: By using an existing profile and remote debugging, the script avoids the "New Login" flags that usually trigger CAPTCHAs.
Data Cleaning: Includes logic to filter out empty tweets or ads depending on the HTML structure.

⚠️ Ethical Note & Disclaimer
This project is for academic and professional research purposes. Scraping Twitter (X) may violate their Terms of Service. Ensure you respect user privacy and do not use the data for malicious intent.
