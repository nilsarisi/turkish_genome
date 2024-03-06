from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def scrape_variant_data_with_selenium(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.

    # Set path to chromedriver as needed

    # Initialize the driver
    driver = webdriver.Chrome()

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the data to load (adjust the selector as necessary)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.variant-container"))
        )

        # Extract the data (adjust selectors based on actual structure)
        variant_containers = driver.find_elements(By.CSS_SELECTOR, "div.variant-container")
        variants = []

        for container in variant_containers:
            variant_id = container.find_element(By.CSS_SELECTOR, ".variant-id").text.strip()
            hgvs_consequence = container.find_element(By.CSS_SELECTOR, ".hgvs").text.strip()
            # Add more fields based on your requirements

            variants.append({
                'Variant ID': variant_id,
                'HGVS Consequence': hgvs_consequence,
                # Add more fields as necessary
            })

        return variants

    finally:
        driver.quit()

# Example usage
url = "https://tgd.tuseb.gov.tr/en/gene/ENSG00000000460"
variant_data = scrape_variant_data_with_selenium(url)
print(variant_data)
