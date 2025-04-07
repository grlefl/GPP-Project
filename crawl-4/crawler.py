import os
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure Selenium Driver
chrome_options = Options(); chrome_options.headless = True  # run in the background
driver = webdriver.Chrome(options=chrome_options)  # start the browser

# Set Up Output CSV File
file_name = os.path.join("./", "output.csv"); file_exists = os.path.isfile(file_name)  # make sure file exists

# Open CSV File for Writing
with open(file_name, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:  # write headers if file is new
        writer.writerow(["Tranko Rank", "Website", "Network IP Address", "State", "GPP String", "Section List", "Serialized Ping"])

    # Record Network IP and State
    network_ip = requests.get("https://api.ipify.org").text
    ip_info = requests.get(f"https://ipinfo.io/{network_ip}/json").json()
    state = ip_info.get("region", "unknown")

    # Read Websites from Input CSV
    with open("1 to 1000.csv", newline="", encoding="utf-8") as f:  # UPDATE THIS PATH
        reader = csv.reader(f, delimiter='\t')

        for row in reader:
            if not row: continue  # skip empty lines

            rank = row[0]; url = row[1]

            if not url.startswith("https://"):
                url = f"https://{url}/"  # should not have to format this

            try:
                # Visit Website URL
                driver.get(url)  # navigate to url
                time.sleep(10)  # wait for page to load
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"); time.sleep(2)  # scroll to trigger lazy loading

                # Check for GPP API and Record Ping Object
                try:
                    gpp_data = driver.execute_script("""
                        return new Promise((resolve) => {
                            if (typeof __gpp === 'function') {
                                __gpp('ping', (data, success) => resolve({ data, success }));
                            } else {
                                resolve("GPP API not found");
                            }
                        });
                    """)
                except Exception as e:
                    gpp_data = {f"Script execution failed: {str(e)}"}

                # Record GPP String
                gpp_string = gpp_data.get("data", {}).get("gppString", "not found")

                # Record SectionList
                section_list = gpp_data.get("data", {}).get("sectionList", [])

            except Exception as e:
                gpp_string = "N/A"
                section_list = "N/A"
                gpp_data = {f"URL execution failed: {str(e)}"}

            # Write Row with Website URL, Network IP, State, and Serialized Ping Data
            writer.writerow([rank, url, network_ip, state, gpp_string, section_list, str(gpp_data)])

driver.quit()  # close browser

