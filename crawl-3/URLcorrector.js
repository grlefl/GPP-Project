const puppeteer = require('puppeteer');
const fs = require('fs');
const csvParser = require('csv-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const inputFile = '9to10k.csv'; // change this to input csv
const outputFile = '9to10k_output.csv'; //change this to desirable output file title 
const prefixes = ['https://', 'http://', 'https://www.', 'http://www.'];

async function checkURL(browser, url) {
    const page = await browser.newPage();
    try {
        const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 10000 });
        return response.status() >= 200 && response.status() < 400;
    } catch (error) {
        console.error(`Error accessing ${url}:`, error.message);
        return false;
    } finally {
        await page.close();
    }
}

async function processCSV() {
    let browser;
    try {
        browser = await puppeteer.launch({ headless: true });

        const results = [];
        const rows = [];

        await new Promise((resolve, reject) => {
            fs.createReadStream(inputFile)
                .pipe(csvParser({ mapHeaders: ({ header }) => header.trim() })) // Trim headers to avoid formatting issues
                .on('data', (row) => {
                    rows.push(row);
                })
                .on('end', resolve)
                .on('error', reject);
        });

        if (rows.length === 0) {
            console.error("No valid rows found in the CSV file. Please check the formatting.");
            return;
        }

        const headers = Object.keys(rows[0]);
        console.log("Detected headers:", headers); // Debugging detected headers

        for (const row of rows) {
            const rank = row[headers[0]]?.trim();
            const domain = row[headers[1]]?.trim();

            if (!rank || !domain || domain.toLowerCase() === 'undefined') {
                console.warn(`Skipping entry due to missing or invalid domain: Rank ${rank}`);
                continue;
            }

            for (const prefix of prefixes) {
                const fullURL = `${prefix}${domain}`;
                const isValid = await checkURL(browser, fullURL);
                if (isValid) {
                    results.push({ Rank: rank, URL: fullURL });
                    break;
                }
            }
        }

        if (results.length === 0) {
            console.warn("No valid URLs found. Check the domains and internet connectivity.");
        } else {
            const csvWriter = createCsvWriter({
                path: outputFile,
                header: [{ id: 'Rank', title: 'Rank' }, { id: 'URL', title: 'URL' }]
            });

            await csvWriter.writeRecords(results);
            console.log(`CSV file created successfully: ${outputFile}`);
        }

    } catch (error) {
        console.error("An error occurred:", error);
    } finally {
        if (browser && browser.isConnected()) {
            try {
                await browser.close();
            } catch (closeError) {
                console.error("Error closing browser:", closeError);
            }
        }
    }
}

processCSV();