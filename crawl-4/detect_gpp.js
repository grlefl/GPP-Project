const puppeteer = require('puppeteer');

async function checkGPP(url) {
    const browser = await puppeteer.launch({
        headless: false, // set to true for headless mode
        // args: ['--proxy-server=44.195.247.145:80', '--ignore-certificate-errors']
    });
    const page = await browser.newPage();

    console.log(`Navigating to ${url}`);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 0 });

    // Scroll down to trigger lazy loading
    await page.evaluate(() => {
        window.scrollTo(0, document.body.scrollHeight);
    });

    console.log("Waiting for 25 seconds...");
    await new Promise(r => setTimeout(r, 1000));

    console.log("Checking for GPP API...");
    const gppData = await page.evaluate(() => {
        return new Promise((resolve) => {
            // if (typeof __gpp !== "function") {
            //     resolve({ error: "GPP API not found" });
            //     return;
            // }

            try {
                __gpp('ping', (data, success) => {
                    console.log('Ping request was successful:', success, data);
                    resolve({ data, success });
                });
            } catch (error) {
                resolve({ error: "Error executing GPP API" });
            }
        });
    });

    console.log("GPP API Response:", gppData);

    await browser.close();
}

const targetUrl = 'http://www.aarp.org/'; // Replace with the actual URL
checkGPP(targetUrl);