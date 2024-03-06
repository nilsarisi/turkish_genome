from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

# Initialize the WebDriver with headless option
def init_driver():
    options = Options()
    options.add_argument('--headless')  # Uncomment for headless
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver

# Function to scrape variants for a specific gene
def scrape_variants(driver, gene_id, gene_url):
    driver.get(gene_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'variant_actual_table')))
    scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.dataTables_scrollBody')
    variants = []
    previous_height = 0

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        WebDriverWait(driver, 10).until(lambda d: previous_height != d.execute_script("return arguments[0].scrollTop", scrollable_div))
        current_height = driver.execute_script("return arguments[0].scrollTop", scrollable_div)
        if current_height == previous_height:
            break
        previous_height = current_height
        new_rows = driver.find_elements(By.CSS_SELECTOR, '#variant_actual_table tbody tr')
        for row in new_rows[len(variants):]:
            variant_data = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
            variants.append([gene_id] + variant_data)

    return variants

# Main orchestration function
def main():
    driver = init_driver()
    try:
        variants = []
        # Assuming you have a list of gene URLs and IDs to process, for example:
        genes = [('gene1_id', 'https://tgd.tuseb.gov.tr/en/chromosome/chr21')] # Placeholder
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_gene = {executor.submit(scrape_variants, driver, gene_id, gene_url): (gene_id, gene_url) for gene_id, gene_url in genes}
            for future in as_completed(future_to_gene):
                gene_data = future_to_gene[future]
                try:
                    gene_variants = future.result()
                    variants.extend(gene_variants)
                except Exception as exc:
                    print('%r generated an exception: %s' % (gene_data, exc))
        
        # Write the collected variant data to CSV
        with open('variants.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Gene ID', 'Variant ID', 'HGVS', 'VEP Annotation', 'Clinical Significance', 'dbSNP (rsID)', 'Homozygote Count', 'Allele Frequency', 'Alternative Allele Count', 'Total Allele Count'])
            for variant in variants:
                writer.writerow(variant)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
