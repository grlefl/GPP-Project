import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Websites to test
websites = [
    "https://www.onetrust.com/blog/global-privacy-platform/", 
    "https://www.iubenda.com"
]

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Enable logging for console output
chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

# Path to ChromeDriver (Replace with your actual path)
CHROME_DRIVER_PATH = "D:/MCS/Sem4/Privacy/Project_1/chromedriver.exe"
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# JavaScript code to inject and execute
js_code = """
try {
    __gpp("ping", function (data, success) {
        console.log("GPP_RESPONSE:" + JSON.stringify(data));
    });
} catch (error) {
    console.log("GPP_ERROR: " + error.message);
}
"""

results = []

# Visit each website and execute JavaScript
for site in websites:
    try:
        driver.get(site)
        time.sleep(5)  # Allow time for page load

        # Execute JavaScript
        driver.execute_script(js_code)
        time.sleep(3)  # Allow JS execution

        # Capture browser console logs
        logs = driver.get_log("browser")
        output = None

        for entry in logs:
            message = entry["message"]
            if "GPP_RESPONSE:" in message:
                output = message.split("GPP_RESPONSE:")[1].strip()
                break
            elif "GPP_ERROR:" in message:
                output = message.strip()
                break
        
        results.append({"Website": site, "Response": output if output else "No Response"})
        print(f"[✓] {site} → {output}")

    except Exception as e:
        print(f"[✗] Error on {site}: {e}")
        results.append({"Website": site, "Response": f"Error: {e}"})

# Close the browser
driver.quit()

# Save results to CSV
csv_file = "gpp_results.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Website", "Response"])
    writer.writeheader()
    writer.writerows(results)

print(f"\nResults saved to {csv_file}")