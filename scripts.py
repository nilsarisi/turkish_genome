from bs4 import BeautifulSoup
import csv

# Load your HTML file content into BeautifulSoup
with open('chromosome_htmls/chr21.html', 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find the table by its ID
table = soup.find('table', id='gene_table')

# Prepare to write to a file
with open('chromosome_tables/chromosome21.csv', 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Write header
    filewriter.writerow(['Gene ID', 'Symbol', 'Region Start', 'Region End', '# Transcripts', '# Variants'])
    
    # Check if the table was found
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if cols:
                gene_id = cols[0].text.strip()
                symbol = cols[1].text.strip()
                region_start = cols[2].text.strip()
                region_end = cols[3].text.strip()
                transcripts = cols[4].text.strip()
                variants = cols[5].text.strip()
                
                # Write row data
                filewriter.writerow([gene_id, symbol, region_start, region_end, transcripts, variants])
    else:
        print("Table not found.")
