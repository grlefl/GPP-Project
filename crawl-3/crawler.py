import os
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure Selenium Driver
chrome_options = Options(); chrome_options.headless = True  # run in the background
chrome_options.add_extension('./gpc_detector.crx') #adds GPC extension to the browser
driver = webdriver.Chrome(options=chrome_options)  # start the browser

# Set Up Output CSV File
file_name = os.path.join("./", "output.csv"); file_exists = os.path.isfile(file_name)  # make sure file exists

# Open CSV File for Writing
with open(file_name, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:  # write headers if file is new
        writer.writerow(["Website", "URL","Network IP Address", "State", "GPP String", "US National API", "National GPC", "Correct Nat GPC", "California API", "California GPC", "Correct CA Gpc", "Has Other Sections", "Other Section List","Section List", "Serialized Ping"])

    # Record Network IP and State
    network_ip = requests.get("https://api.ipify.org").text
    ip_info = requests.get(f"https://ipinfo.io/{network_ip}/json").json()
    state = ip_info.get("region", "unknown")



    # Read Websites from Input CSV
    with open("../crawl-1/Results/1 to 1000.csv", newline="\n", encoding="utf-8") as f:  # UPDATE THIS PATH
        reader = csv.reader(f)

        for row in reader:
            if not row: continue  # skip empty lines

            # Record Website URL
            rank = row[0] #save website's Tranco rank
            url = row[1]; driver.get(url)  # navigate to url
            time.sleep(10)  # wait for page to load
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"); time.sleep(2)  # scroll to trigger lazy loading

            # Check for GPP API and Record Ping Object
            try:
                gpp_data = driver.execute_script("""
                    return new Promise((resolve) => {
                        if (typeof __gpp === 'function') {
                            __gpp('ping', (data, success) => resolve({ data, success }));
                        } else {
                            resolve({ error: "GPP API not found" });
                        }
                    });
                """)
            except Exception as e:
                gpp_data = {"error": f"Script execution failed: {str(e)}"}

            # Record GPP String
            gpp_string = gpp_data.get("data", {}).get("gppString", "not found")

            has_nat = False
            has_ca = False
            nat_gpc = False
            ca_gpc = False
            has_other_section = False

            other_sections = []


            if 'data' in gpp_data.keys():
                if 'usnat' in gpp_data['data']['parsedSections'].keys() or 'usnatv1' in gpp_data['data']['parsedSections'].keys():
                    has_nat = True
                if 'usca' in gpp_data['data']['parsedSections'].keys():
                    has_ca = True
                
                for i in gpp_data['data']['parsedSections'].keys():
                    if i != 'usnat' and i != 'usnatv1' and i != 'usca':
                        has_other_section = True
                        other_sections.append(i)
            if has_nat:
                try:
                    nat_gpc = gpp_data['data']['parsedSections']['usnat']['Gpc']
                except:
                    nat_gpc = gpp_data['data']['parsedSections']['usnatv1']['Gpc']
            if has_ca:
                ca_gpc = gpp_data['data']['parsedSections']['usca']['Gpc']
            if not (nat_gpc or ca_gpc):
                gpc_signal = 'No national or california section'
            # Record SectionList
            section_list = gpp_data.get("data", {}).get("sectionList", [])

            # Write Row with Website URL, Network IP, State, and Serialized Ping Data
            writer.writerow([rank, url, network_ip, state, gpp_string, has_nat, nat_gpc, (has_nat and nat_gpc),has_ca, ca_gpc, (has_ca and ca_gpc), has_other_section, other_sections, section_list, str(gpp_data)])

driver.quit()  # close browser

