from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def init_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--incognito')  # Run in incognito mode
    options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images
    driver = webdriver.Chrome(options=options)
    return driver

def save_links_with_scrolling(url, file_name):
    driver = init_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'gene_table')))
        
        scrollable_div = driver.find_element(By.XPATH, '//*[@id="gene_table"]/ancestor::div[contains(@class, "dataTables_scrollBody")]')
        previous_scroll_height = 0
        while True:
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + 2000;', scrollable_div)
            time.sleep(0.1)  # Reduced sleep time
            new_scroll_height = driver.execute_script('return arguments[0].scrollTop;', scrollable_div)
            if new_scroll_height == previous_scroll_height:
                break
            previous_scroll_height = new_scroll_height
        
        links = driver.find_elements(By.CSS_SELECTOR, '#gene_table tbody tr td a')
        
        with open(file_name, 'w') as file:
            for link in links:
                file.write(link.get_attribute('href') + '\n')
                
        print(f"Links have been saved to {file_name}")
        
    finally:
        driver.quit()

# Define the range of chromosomes you're interested in
chromosomes = range(1, 23)  # Adjust the range as necessary

for i in chromosomes:
    url = f"https://tgd.tuseb.gov.tr/en/chromosome/chr{i}"  # Adjust the base URL as needed
    file_name = f"gene_links_chr{i}.txt"
    save_links_with_scrolling(url, file_name)
    print(f"Completed chromosome {i}")
