import os
import time
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROME_DRIVER_PATH = "D:/AAAA/New folder/chromedriver.exe"
URL_DIR = "./url_tranco_6k"
OUTPUT_DIR = "./output_tranco_3000_usp"
MAX_WORKERS = 8

# JavaScript for USP API "ping" check
js_code = """
try {
  __uspapi('ping', 1, function(resp, success) {
    console.log('USPAPI_PING:' + JSON.stringify({resp, success}));
  });
} catch (e) {
  console.log('USPAPI_ERROR:' + e.message);
}
"""

# Load websites from file, in batches of 100
def load_websites(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        websites = [line.strip() for line in f if line.strip()]
    return list(set(websites))

# Headless Chrome WebDriver
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

# Main function for USP API presence
def check_usp(domain):
    driver = get_driver()
    result = {
        "Website": domain,
        "USP_Ping": "",
        "USP_Response": ""
    }
    #Try URLs, pick first one that works
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
            result["Website"] = url
            success = True
            break
        except Exception:
            continue

    if not success:
        result["USP_Response"] = "Site load failed"
        print(f"Failed to load any URL format for: {domain}")
        driver.quit()
        return result

    try:
        driver.execute_script(js_code)
        time.sleep(3)

        logs = driver.get_log("browser")
        for entry in logs:
            msg = entry["message"]
            if "USPAPI_PING:" in msg:
                result["USP_Response"] = msg.split("USPAPI_PING:")[1].strip()
                break
            elif "USPAPI_ERROR:" in msg:
                result["USP_Response"] = msg.strip()
                break

        if not result["USP_Response"]:
            result["USP_Response"] = "No Response"

        print(f"{result['Website']} → USP: {result['USP_Response']}")

    except Exception as e:
        result["USP_Response"] = f"Error: {e}"
        print(f"Error after loading {result['Website']}: {e}")
    finally:
        driver.quit()

    return result

# Run checks in parallel
def run_parallel(websites):
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_usp, site) for site in websites]
        for future in as_completed(futures):
            results.append(future.result())
    return results

# Save results (CSV + JSON + inaccessible list)
def save_results(results, filename_without_ext):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    simplified_results = []
    inaccessible = []

    for r in results:
        url = r["Website"]
        response = r.get("USP_Response", "")
        ping = "true" if response.startswith("{") else "false"

        simplified_results.append({
            "url (name)": url,
            "ping": ping
        })

        if response == "Site load failed":
            inaccessible.append(url)

    #csv
    csv_path = os.path.join(OUTPUT_DIR, f"{filename_without_ext}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["url (name)", "ping"])
        writer.writeheader()
        writer.writerows(simplified_results)
    
    #json
    json_path = os.path.join(OUTPUT_DIR, f"{filename_without_ext}_raw.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    #Inaccessible list
    if inaccessible:
        txt_path = os.path.join(OUTPUT_DIR, f"inaccessible_{filename_without_ext}")
        with open(txt_path, "w", encoding="utf-8") as f:
            for site in inaccessible:
                f.write(site + "\n")
        print(f"Inaccessible sites saved to {txt_path}")
    else:
        print("All sites loaded successfully — no inaccessible list generated.")

    print(f"\nResults saved to {csv_path} and {json_path}\n")

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
