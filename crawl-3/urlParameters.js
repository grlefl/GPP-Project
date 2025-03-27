const puppeteer = require('puppeteer');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

(async () => {
    // Launch the browser
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    // list of URLs
    const urls = ['https://www.washingtonpost.com/world/2025/03/27/zelensky-trump-ukraine-russia-negotiations/', 
    'https://www.washingtonpost.com/politics/2025/03/26/trump-presidency-news/', 
    'https://www.washingtonpost.com/politics/2025/03/26/signal-conspiracy-theory-trump-waltz/',];

    // change to GPP 
    const keyword = "GPP";

    const checkURLForKeyword = (url, keyword) => {
        return url.toLowerCase().includes(keyword.toLowerCase());
    };

    // to save matched URLs into a list 
    const matchedURLs = [];

    // Looks through list of URLs (defined above) to match to GPP
    for (const url of urls) {
        await page.goto(url, {waitUntil: 'networkidle2', timeout: 0});

        if (checkURLForKeyword(url, keyword)) {
            matchedURLs.push({ url });
        }
    }

     // Define CSV file structure
     const csvWriter = createCsvWriter({
        path: './matched_urls.csv', // File name
        header: [
            { id: 'url', title: 'URLs' }, // CSV column header
        ],
    });

    // Write matched URLs to CSV
    await csvWriter.writeRecords(matchedURLs);
    
    await browser.close();
})();