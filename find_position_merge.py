import pandas as pd
import re
from intervaltree import IntervalTree

# Load the data
variants_df = pd.read_csv("variants_tables/chr6_Var.csv")
transcripts_df = pd.read_csv("updated_transcripts_tables/transcripts_chr6.csv")

# Function to extract position using regex (already optimized by handling NaN and conversion inside the function)
def extract_position(hgvs_str):
    if pd.isna(hgvs_str):
        return None
    match = re.search(r'g\.(\d+)', str(hgvs_str))
    return int(match.group(1)) if match else None

# Vectorize the position extraction
variants_df['Position'] = variants_df['HGVS Consequence'].astype(str).apply(extract_position)

# Create an interval tree from the transcripts data for fast range querying
tree = IntervalTree()
for _, row in transcripts_df.iterrows():
    tree[row['Region Start']:row['Region End']] = row['Transcript ID']

# Function to find the transcript ID using the interval tree
def find_transcript_id(position):
    if position is None:
        return None
    intervals = tree[position]
    return next(iter(intervals), None).data if intervals else None

# Vectorize the function to find transcripts based on position
variants_df['Transcript ID'] = variants_df['Position'].apply(find_transcript_id)

print(variants_df[['Position', 'Transcript ID']])

# Load data
chromosome_df = pd.read_csv('gene_tables/chromosome6.csv')

# Merge transcripts with chromosomes
transcripts_df = transcripts_df.merge(chromosome_df, left_on='Gene Symbol', right_on='Symbol')

# Merge variants with transcripts
transcripts_df = transcripts_df.merge(variants_df, on='Transcript ID')

# Drop duplicates across the entire DataFrame to clean up before filtering by Variant ID
transcripts_df = transcripts_df.drop_duplicates()

# Drop duplicates based on 'Variant ID' to ensure only unique variants are retained
transcripts_df = transcripts_df.drop_duplicates(subset=['Variant ID'], keep='first')

# Optionally print the DataFrame to verify the results
print(transcripts_df)

# Save the cleaned and processed DataFrame to a CSV file
transcripts_df.to_csv('chr6_all.csv', index=False)
