from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time
import concurrent.futures
import threading

# Initialize a threading lock
lock = threading.Lock()

# Function to scrape variant table
def scrape_variant_table(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(0.3)

    variant_table = driver.find_element(By.ID, 'variant_actual_table')
    scrollable_div = variant_table.find_element(By.XPATH, './ancestor::div[contains(@class, "dataTables_scrollBody")]')

    # Acquire the lock before writing to the file
    with lock:
        with open('variants_combined.csv', 'a', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            previous_scroll_height = 0
            while True:
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + 1000;', scrollable_div)
                time.sleep(0.05)
                new_scroll_height = driver.execute_script('return arguments[0].scrollTop;', scrollable_div)
                if new_scroll_height == previous_scroll_height:
                    break
                previous_scroll_height = new_scroll_height

            rows = variant_table.find_elements(By.CSS_SELECTOR, 'tbody tr')
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, 'td')
                if cols:
                    data = [col.text.strip() for col in cols]
                    filewriter.writerow(data[:9])  # Write data

    driver.quit()

# Prepare the CSV file with headers before starting the threads
with open('variants_combined.csv', 'w', newline='', encoding='utf-8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Variant ID', 'HGVS Consequence', 'VEP Annotation', 'Clinical Significance', 'dbSNP (rsID)', 'Number of Homozygous', 'Allele Frequency', 'Allele Count', 'Allele Number'])

# Read URLs from the text file
with open('gene_links/gene_links_chr1.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

# Use ThreadPoolExecutor to run multiple instances of the function in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scrape_variant_table, urls)
