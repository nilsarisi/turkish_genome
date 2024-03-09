from playwright.async_api import async_playwright, TimeoutError
import asyncio
import csv

async def scrape_with_playwright(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, timeout=30000)  # Set a specific timeout for page loading
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
    except TimeoutError as e:
        print(f"Timeout error encountered for URL {url}. Retrying in 5 minutes...")
        await asyncio.sleep(300)  # Wait for 5 minutes before retrying
        return await scrape_with_playwright(url)  # Recursive call to retry
    except Exception as e:
        print(f"An error occurred for URL {url}: {str(e)}. Retrying in 5 minutes...")
        await asyncio.sleep(300)  # Wait for 5 minutes before retrying
        return await scrape_with_playwright(url)  # Recursive call to retry

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
            if data:  # Check if data is not None or empty
                filewriter.writerows(data)
            count += 1
            if count % 50 == 0:  # Check if the count is a multiple of 100
                print(f"{count} links are done")

        if count % 50 != 0:  # To print the final count if it's not a multiple of 100
            print(f"{count} links are done")

# Specify your input file with URLs and output CSV file
input_file = 'gene_links/gene_links_chr2.txt'
output_file = 'chr2_Var.csv'

# Run the scraping and writing process
asyncio.run(scrape_urls_and_write_to_csv(input_file, output_file))
