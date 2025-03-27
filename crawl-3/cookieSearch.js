const puppeteer = require('puppeteer');
const fs = require('fs');
const csv = require('csv-parser');

(async () => {
    // Read URLs from external CSV and return them as an array
    const readUrlsFromCsv = (filePath) => {
        return new Promise((resolve, reject) => {
            const urls = [];
            fs.createReadStream(filePath)
                .pipe(csv())
                .on('data', (row) => {
                    // Assuming the CSV has a column named "url" -- change to whatever the column is named
                    if (row.url) {
                        urls.push(row.url);
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
        const filePath = 'urls.csv'; // Path to your CSV file -- change to whatever it is called
        const urls = await readUrlsFromCsv(filePath);

        const browser = await puppeteer.launch({ headless: false });
        const page = await browser.newPage();

        // Iterate through URLs and check for cookies containing "gpp"
        for (const url of urls) {
            console.log(`Visiting: ${url}`);
            try {
                await page.goto(url, { waitUntil: 'domcontentloaded' });

                // Retrieve cookies for the current page -- this does not search through httpOnly cookies
                // puppeteer doesn't support some easier methods
                //const cookies = await page.cookies();
                
                // this should imitate searching through all cookies ?
                const client = await page.target().createCDPSession();
                const cookies = (await client.send('Network.getAllCookies')).cookies;

                // check if any cookie contains "gpp"
                const matchingCookies = cookies.filter(cookie => cookie.name.toLowerCase().includes('gpp') 
                || cookie.value.toLowerCase().includes('gpp'));

                if (matchingCookies.length > 0) {
                    console.log(`Cookies matching "gpp" found on ${url}:`);
                    matchingCookies.forEach(cookie => console.log(`${cookie.name}: ${cookie.value}`));
                } else {
                    console.log(`No cookies containing "gpp" found on ${url}.`);
                }
            } catch (error) {
                console.error(`Error visiting ${url}:`, error);
            }
        }

        await browser.close();
    } catch (error) {
        console.error('An error occurred:', error);
    }
})();