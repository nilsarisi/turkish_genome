# turkish_genome

- Drive link for folders of scraped data: https://drive.google.com/drive/folders/10JfiX4G_cke3GySrZ9frLkwtyKpnpciR?usp=sharing

About the Project

-  The Turkey National Genome and Bioinformatics Project, spearheaded by TÜSEB (the Presidency of the Institutes of Health of Turkey), is a landmark initiative aimed at elucidating the molecular underpinnings of diseases, advancing diagnostics and therapeutic interventions, and laying the groundwork for personalized medicine. Leveraging Whole Genome, Whole Transcriptome, and metagenome sequencing, the project seeks to map the genetic diversity within the Turkish population and compare it with global datasets to enhance our understanding of genetic factors in disease.


Data Acquisition Challenges
-  While embarking on this ambitious journey, we encountered a critical challenge: discrepancies between the data reported on the website and our findings. This issue stems from inaccuracies in the website's presentation rather than in our data processing methodologies. 

Data Acquisiton Process

Gene Information Extraction: script_gene_table.py
-	Tool Used: BeautifulSoup
-	Scope: Extracted gene information across 22 chromosomes, aiming to understand the genetic basis and structure.

Transcript Information Collection: script_transcript_table.py
-	Tool Used: Selenium
-	Scope: Gathered detailed transcript information for the 22 chromosomes to further dissect gene expression and functionality.

Variant Information Compilation: script_variant_crashproof, script_variants_asynch.py, variant_10threads.py
-	Tool Used: Playwright
-	Scope: Acquired variant information from every gene across 22 chromosomes, crucial for identifying genetic variations and their implications on health.

Miscellaneous scripts: create_linktxts.py for scraping variants' links to fasten the variant scraping process and csvfile.py to create necessary csv files.

Future Directions
-  Understanding and rectifying the data presentation issues on the website are ongoing. We are committed to transparency and accuracy as we advance towards making significant contributions to genomics and personalized medicine.
