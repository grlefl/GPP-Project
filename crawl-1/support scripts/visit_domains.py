import os
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#checks if a list of urls can be visited by a user.
# Configuration
CHROME_DRIVER_PATH = "D:/MCS/Sem4/Privacy/Project_1/early/chromedriver.exe"
URL_DIR = "./url_tranco"
OUTPUT_DIR = "./output_tranco_success"
MAX_WORKERS = 5

# Load domains from a file
def load_domains(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return list(set(line.strip() for line in f if line.strip()))

# Get Chrome WebDriver (headless)
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)

# Try all URL variations for a domain
def check_website_success(domain):
    tried_urls = [
        f"https://{domain}",
        f"http://{domain}",
        f"https://www.{domain}",
        f"http://www.{domain}"
    ]

    driver = get_driver()
    result = {
        "Domain": domain,
        "Success": False,
        "Working_URL": ""
    }

    for url in tried_urls:
        try:
            driver.get(url)
            time.sleep(2)
            result["Success"] = True
            result["Working_URL"] = url
            print(f"{domain} → Loaded: {url}")
            break  # Stop after first success
        except Exception as e:
            print(f"{domain} → Failed: {url} → {e}")
    
    driver.quit()
    return result

# Run domain checks in parallel
def run_parallel(domains):
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_website_success, domain) for domain in domains]
        for future in as_completed(futures):
            results.append(future.result())
    return results

# Save results to CSV
def save_results(results, filename_without_ext):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    csv_path = os.path.join(OUTPUT_DIR, f"{filename_without_ext}.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Domain", "Success", "Working_URL"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults saved to {csv_path}\n")

# Process all .txt files in the input folder
def process_all_files():
    if not os.path.exists(URL_DIR):
        print(f"URL directory not found: {URL_DIR}")
        return

    files = sorted([f for f in os.listdir(URL_DIR) if f.endswith(".txt")])
    print(f"Found {len(files)} input files.\n")

    for file in files:
        print(f"=== Processing file: {file} ===")
        domains = load_domains(os.path.join(URL_DIR, file))
        print(f"Loaded {len(domains)} unique domains.")

        results = run_parallel(domains)
        filename_without_ext = os.path.splitext(file)[0]
        save_results(results, filename_without_ext)

# Entry point
if __name__ == "__main__":
    process_all_files()