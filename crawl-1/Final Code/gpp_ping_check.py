import os
import time
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROME_DRIVER_PATH = "D:/MCS/Sem4/Privacy/Project_1/early/chromedriver.exe"
URL_DIR = "./url_tranco"
OUTPUT_DIR = "./output_tranco_2"
MAX_WORKERS = 20

#JavaScript to check GPP
js_code = """
try {
    __gpp("ping", function (data, success) {
        console.log("GPP_RESPONSE:" + JSON.stringify(data));
    });
} catch (error) {
    console.log("GPP_ERROR: " + error.message);
}
"""

#Load websites from file
def load_websites(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        websites = [line.strip() for line in f if line.strip()]
    return list(set(websites))

#Get Chrome WebDriver
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

#GPP + Cookie Checker
def check_gpp_and_cookie(domain):
    driver = get_driver()
    result = {
        "Website": domain,
        "GPP_Response": "",
        "OTGPPConsent_Cookie": "Not Found"
    }

    tried_urls = [
        f"https://{domain}",
        f"http://{domain}",
        f"https://www.{domain}",
        f"http://www.{domain}"
    ]

    success = False
    for url in tried_urls:
        try:
            driver.get(url)
            time.sleep(5)
            success = True
            result["Website"] = url
            break
        except Exception as e:
            continue

    if not success:
        result["GPP_Response"] = "Site load failed"
        print(f"Failed to load any URL format for: {domain}")
        driver.quit()
        return result

    try:
        # Run GPP check
        driver.execute_script(js_code)
        time.sleep(3)

        logs = driver.get_log("browser")
        for entry in logs:
            msg = entry["message"]
            if "GPP_RESPONSE:" in msg:
                result["GPP_Response"] = msg.split("GPP_RESPONSE:")[1].strip()
                break
            elif "GPP_ERROR:" in msg:
                result["GPP_Response"] = msg.strip()
                break
        if not result["GPP_Response"]:
            result["GPP_Response"] = "No Response"

        # Check for OTGPPConsent cookie
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie["name"] == "OTGPPConsent":
                result["OTGPPConsent_Cookie"] = cookie["value"]
                break

        print(f"{result['Website']} → GPP: {result['GPP_Response']} | OTGPPConsent: {result['OTGPPConsent_Cookie']}")
    except Exception as e:
        result["GPP_Response"] = f"Error: {e}"
        print(f"Error after loading {result['Website']}: {e}")
    finally:
        driver.quit()

    return result


#Run in Parallel
def run_parallel(websites):
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_gpp_and_cookie, site) for site in websites]
        for future in as_completed(futures):
            results.append(future.result())
    return results

#Save Results
def save_results(results, filename_without_ext):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    simplified_results = []
    for r in results:
        url = r["Website"]
        gpp = "true" if "GPP_RESPONSE:" in r["GPP_Response"] or r["GPP_Response"].startswith("{") else "false"
        cookie = "true" if r["OTGPPConsent_Cookie"] != "Not Found" else "false"
        simplified_results.append({
            "url (name)": url,
            "ping": gpp,
            "cookie": cookie
        })

    # Save simplified CSV
    csv_path = os.path.join(OUTPUT_DIR, f"{filename_without_ext}.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["url (name)", "ping", "cookie"])
        writer.writeheader()
        writer.writerows(simplified_results)

    #Save raw JSON
    json_path = os.path.join(OUTPUT_DIR, f"{filename_without_ext}_raw.json")
    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {csv_path} and {json_path}\n")

#Process All URL Files
def process_all_files():
    if not os.path.exists(URL_DIR):
        print(f"URL directory not found: {URL_DIR}")
        return

    files = sorted([f for f in os.listdir(URL_DIR) if f.endswith(".txt")])
    print(f"Found {len(files)} input files.\n")

    for file in files:
        file_path = os.path.join(URL_DIR, file)
        filename_without_ext = os.path.splitext(file)[0]

        print(f"=== Processing file: {file} ===")
        websites = load_websites(file_path)
        print(f"Loaded {len(websites)} unique websites.")

        results = run_parallel(websites)
        save_results(results, filename_without_ext)

if __name__ == "__main__":
    process_all_files()