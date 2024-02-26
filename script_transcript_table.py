from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time

# Initialize the WebDriver


i = 19
while i < 23:
    driver = webdriver.Chrome()
    url = 'https://tgd.tuseb.gov.tr/tr/chromosome/chr' + str(i)

    # Open the target URL
    driver.get(url)

    # Wait for the page to load
    time.sleep(15)

    # Locate the transcript table
    transcript_table = driver.find_element(By.ID, 'transcript_table')

    # Find the scrollable div that contains the transcript table
    scrollable_div = transcript_table.find_element(By.XPATH, './ancestor::div[contains(@class, "dataTables_scrollBody")]')

    csv_file = 'transcripts_chr' + str(i) + '.csv'

    # Prepare to write to a file
    with open(csv_file, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write header
        filewriter.writerow(['Transcript ID', 'Region Start', 'Region End', '# Variants'])

        # Initialize a variable to track the previous scroll height
        previous_scroll_height = 0
        control = True

        while True:
            # Scroll down within the table
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + 3000;', scrollable_div)
            
            # Wait for the table to load more rows
            time.sleep(0.1)

            # Get the new scroll height
            new_scroll_height = driver.execute_script('return arguments[0].scrollTop;', scrollable_div)

            # Check if we have reached the bottom of the table
            if new_scroll_height == previous_scroll_height:
                break
                # We have reached the bottom of the table

            # Update the previous scroll height for the next iteration
            previous_scroll_height = new_scroll_height

        # After scrolling through the whole table, we collect the data
        rows = transcript_table.find_elements(By.CSS_SELECTOR, 'tbody tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if cols:
                transcript_id = cols[0].text.strip()
                region_start = cols[1].text.strip()
                if cols[2].text is not None:
                    region_end = cols[2].text.strip()
                variants = cols[3].text.strip() if len(cols) > 3 else 'N/A'
                
                # Write row data
                filewriter.writerow([transcript_id, region_start, region_end, variants])
    i = i + 1
    driver.quit()
    


# Close the WebDriver
