import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Read domains
with open("D:/AAAA/websites100.txt", "r") as f:
    base_domains = [line.strip() for line in f]

# Try these variants (with trailing slash)
prefixes = ["https://", "https://www.", "http://", "http://www."]

# Chrome config
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

CHROME_DRIVER_PATH = "D:/AAAA/New folder/chromedriver.exe"
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# JS code to inject
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
hasGpp = []
fail_count = 0

for domain in base_domains:
    site_handled = False
    for prefix in prefixes:
        site = prefix + domain + "/"
        try:
            driver.get(site)
            time.sleep(5)

            driver.execute_script(js_code)
            time.sleep(3)

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
            if output and "gppVersion" in output:
                hasGpp.append(site)

            site_handled = True
            break  # Stop trying other variants

        except Exception as e:
            print(f"[✗] Failed: {site}: {e}")

    if not site_handled:
        fail_count += 1
        results.append({"Website": domain, "Response": "All variants failed"})
        print(f"[✗] All variants failed for {domain}")

driver.quit()

# Save to CSV
csv_file = "gpp_results.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Website", "Response"])
    writer.writeheader()
    writer.writerows(results)

print(f"\nResults saved to {csv_file}")
print(f"Websites with GPP support: {(hasGpp)}")
print(f"Websites with GPP support: {len(hasGpp)}")
print(f"Websites with all variants failed: {fail_count}")
