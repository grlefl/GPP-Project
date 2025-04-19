const puppeteer = require('puppeteer');
const fs = require('fs');
const csv = require('csv-parser');
const { parse } = require('json2csv');

(async () => {
    // Read URLs from external CSV and return them as an array
    const readUrlsFromCsv = (filePath) => {
        return new Promise((resolve, reject) => {
            const urls = [];
            fs.createReadStream(filePath)
                .pipe(csv())
                .on('data', (row) => {
                    //if (row["url (name)"]) {
                     //   urls.push(row["url (name)"]);
                        // if (row.URL) {
                            // urls.push(row.URL));}  USE THIS FOR column titled URL
                    if (row.URL) {
                        urls.push(row.URL); 
                    }
                })
                .on('end', () => {
                    resolve(urls);
                })
                .on('error', (error) => {
                    reject(error);
                });
        });
    };

    try {
        const filePath = '7to8k_output.csv'; // Path to your CSV file
        const outputFilePath = '7to8k_cookies.csv'; // Output CSV file
        const urls = await readUrlsFromCsv(filePath);
        const browser = await puppeteer.launch({ headless: false });
        const page = await browser.newPage();
        const allCookies = [];

        for (const url of urls) {
            console.log(`Visiting: ${url}`);
            try {
                await page.goto(url, { waitUntil: 'domcontentloaded' });

                // Retrieve cookies for the current page
                const client = await page.target().createCDPSession();
                const cookies = (await client.send('Network.getAllCookies')).cookies;

                // Check for cookies containing "gpp"
                const matchingCookies = cookies.filter(cookie => 
                    cookie.name.includes('OTGPPConsent')
                    //cookie.value.toLowerCase().includes('gpp')
                );

                if (matchingCookies.length > 0) {
                    matchingCookies.forEach(cookie => {
                        allCookies.push({
                            url,
                            name: cookie.name,
                            value: cookie.value,
                            domain: cookie.domain,
                            path: cookie.path,
                            expires: cookie.expires,
                            httpOnly: cookie.httpOnly,
                            secure: cookie.secure,
                            sameSite: cookie.sameSite
                        });
                    });
                }
            } catch (error) {
                console.error(`Error visiting ${url}:`, error);
            }
        }

        await browser.close();

        // Write to CSV file
        if (allCookies.length > 0) {
            const csvString = parse(allCookies, { fields: ["url", "name", "value", "domain", "path", "expires", "httpOnly", "secure", "sameSite"] });
            fs.writeFileSync(outputFilePath, csvString);
            console.log(`Cookies saved to ${outputFilePath}`);
        } else {
            console.log("No matching cookies found.");
        }

    } catch (error) {
        console.error('An error occurred:', error);
    }
})();