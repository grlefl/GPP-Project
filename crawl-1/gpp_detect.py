import selenium 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

#Websites to crawl. Change to text file format. 
websites = [
    "https://www.onetrust.com/blog/global-privacy-platform/", 
"https://www.iubenda.com/en/help/79212-global-privacy-platform-what-you-need-to-know", 
"https://iabtechlab.com/gpp/", 
"https://www.enzuzo.com/blog/best-data-privacy-management-software", 
"https://termly.io/", 
"https://www.adformhelp.com/hc/en-us/articles/22101384046481-Learn-About-Global-Privacy-Platform", 
"https://www.didomi.io/blog/global-privacy-platform-gpp", 
"https://trustarc.com/", 
"https://www.uniconsent.com/gpp", 
"https://usercentrics.com/knowledge-hub/global-privacy-platform/" 
]


chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
CHROME_DRIVER_PATH = "D:/AAAA/chromedriver.exe"
service = Service(CHROME_DRIVER_PATH)  

driver = webdriver.Chrome(service=service, options=chrome_options)

selected_websites = []

#Javascript
js_code = """
try {
    __gpp('ping', (data, success) => {
        console.log(data); 
    });
} catch (error) {
    console.log(error);
}
"""

for site in websites:
    try:
        driver.get(site)
        time.sleep(3)  #Wait for the page to load
        
        response = driver.execute_script(f"return (function() {{ {js_code} }})()")
        
        if response and "not defined" not in str(response):
            selected_websites.append(site)
    except Exception as e:
        print(f"Error processing {site}: {e}")

#Close the browser
driver.quit()

print("Selected websites:", selected_websites)