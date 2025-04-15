import os
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# configure Selenium Firefox driver
ff_options = webdriver.FirefoxOptions()
ff_options.headless = True  # run in the background
ff_options.set_preference('privacy.globalprivacycontrol.enabled', True)  # add GPC extension
driver = webdriver.Firefox(options=ff_options)  # start the browser

# set up output csv file
file_name = os.path.join("./", "output.csv"); file_exists = os.path.isfile(file_name)  # make sure file exists

# open csv file for writing
with open(file_name, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:  # write headers if file is new
        writer.writerow(["Tranko Rank", "Website", "Network IP Address", "State", "GPP String", "Section List", "GPC Signal", "Serialized Ping", "Error"])

    # record Network IP and State
    network_ip = requests.get("https://api.ipify.org").text
    ip_info = requests.get(f"https://ipinfo.io/{network_ip}/json").json()
    state = ip_info.get("region", "unknown")

    # read websites from input csv
    with open("1 to 1000.csv", newline="", encoding="utf-8") as f:  # UPDATE THIS PATH
        reader = csv.reader(f, delimiter='\t')

        for row in reader:
            if not row: continue  # skip empty lines
            rank = row[0]; url = row[1]  # get Tranco rank and url
            if not url.startswith("https://"): url = f"https://{url}/"  # should not have to format this
            gpp_ping = None; gpp_string = None; section_list = None; gpc_signal = None; error = None  # initialize uncertain variables

            try:
                driver.get(url)  # navigate to url
                time.sleep(10)  # wait for page to load
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"); time.sleep(2)  # scroll to trigger lazy loading

                # check for GPP API and record 'ping' object
                try:
                    gpp_ping = driver.execute_script("""
                        return new Promise((resolve) => {
                            if (typeof __gpp === 'function') {
                                __gpp('ping', (data, success) => resolve({ data, success }));
                            } else {
                                resolve("GPP API not found");
                            }
                        });
                    """)
                    gpp_string = gpp_ping['data']['gppString']  # get GPP string
                    section_list = gpp_ping['data']['sectionList']  # get sectionList
                    try: gpc_signal = gpp_ping['data']['parsedSections']['usnat']['Gpc']
                    except KeyError as e: error = f"GPC Retrieval Error: {str(e)}"
                    gpp_ping = str(gpp_ping)  # serialize ping object
                except Exception as e:
                    error = f"GPP Retrieval Error: {str(e)}"

            except Exception as e:
                error = f"Domain Retrieval Error: {str(e)}"

            # write row with Website URL, Network IP, State, and Serialized Ping Data
            writer.writerow([rank, url, network_ip, state, gpp_string, section_list, gpc_signal, gpp_ping, error])

driver.quit()  # close browser