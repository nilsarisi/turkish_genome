from playwright.async_api import async_playwright
import asyncio
import csv

async def scrape_with_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector('#variant_actual_table')  # Wait for the table to load
        
        # Extract the data
        data = await page.query_selector_all('#variant_actual_table tr')
        extracted_data = []
        for row in data[1:]:  # Skip header row
            cells = await row.query_selector_all('td')
            row_data = [await cell.inner_text() for cell in cells]
            extracted_data.append(row_data[:9])  # Collect first 9 columns of data
        
        await browser.close()
        return extracted_data

async def scrape_urls_and_write_to_csv(input_file, output_file):
    # Read URLs from the text file
    with open(input_file, 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    # Prepare the CSV file with headers
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Variant ID', 'HGVS Consequence', 'VEP Annotation', 'Clinical Significance', 'dbSNP (rsID)', 'Number of Homozygous', 'Allele Frequency', 'Allele Count', 'Allele Number'])

        # Scrape data from each URL and keep track of the count
        count = 0
        for url in urls:
            data = await scrape_with_playwright(url)
            filewriter.writerows(data)
            count += 1
            if count % 10 == 0:  # Check if the count is a multiple of 10
                print(f"{count} links are done")

        if count % 10 != 0:  # To print the final count if it's not a multiple of 10
            print(f"{count} links are done")

# Specify your input file with URLs and output CSV file
input_file = 'gene_links/gene_links_chr21.txt'
output_file = 'chr21_Var.csv'

# Run the scraping and writing process
asyncio.run(scrape_urls_and_write_to_csv(input_file, output_file))
