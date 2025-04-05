const puppeteer = require('puppeteer');
const fs = require('fs');
const csv = require('csv-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

(async () => {
    // Read URLs from CSV file
    const readUrlsFromCsv = (filePath) => {
        return new Promise((resolve, reject) => {
            const urls = [];
            fs.createReadStream(filePath)
                .pipe(csv())
                .on('data', (row) => {
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
        const filePath = '1000results.csv'; // Input CSV file
        const outputFilePath = 'matchedUrls.csv'; // Output CSV file
        const keyword = "GPP";
        const urls = await readUrlsFromCsv(filePath);

        const browser = await puppeteer.launch({ headless: false });
        const page = await browser.newPage();
        const matchedURLs = [];

        // Function to check if URL contains the keyword
        const checkURLForKeyword = (url, keyword) => {
            return url.toLowerCase().includes(keyword.toLowerCase());
        };

        for (const url of urls) {
            // await page.goto(url, { waitUntil: 'networkidle2', timeout: 0 });
            try {
                await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
            } catch (error) {
                console.error(`Skipping ${url} due to timeout:`, error);
            }

            if (checkURLForKeyword(url, keyword)) {
                matchedURLs.push({ url });
            }
        }

        await browser.close();

        // Define CSV writer for output
        const csvWriter = createCsvWriter({
            path: outputFilePath,
            header: [{ id: 'url', title: 'URLs' }],
        });

        // Write matched URLs to CSV
        if (matchedURLs.length > 0) {
            await csvWriter.writeRecords(matchedURLs);
            console.log(`Matched URLs saved to ${outputFilePath}`);
        } else {
            console.log("No matching URLs found.");
        }
        
    } catch (error) {
        console.error('An error occurred:', error);
    }
})();
