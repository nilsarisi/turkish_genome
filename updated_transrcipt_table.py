import pandas as pd

def find_gene_symbol(trans_start, trans_end, genes):
    """Return the gene symbol for overlapping genes."""
    overlap = genes[(genes['Region Start'] <= trans_end) & (genes['Region End'] >= trans_start)]
    if not overlap.empty:
        return overlap['Symbol'].iloc[0]  # Returns the first matching gene symbol
    return "No Match"  # Return 'No Match' if no overlapping gene is found

# Process each chromosome's data
for i in range(1, 23):
    # Load the transcripts and genes DataFrames
    transcripts = pd.read_csv(f'transcripts_chr{i}.csv')
    genes = pd.read_csv(f'chromosome{i}.csv')
    
    # Add a new column 'Gene Symbol' to the transcripts DataFrame
    transcripts['Gene Symbol'] = transcripts.apply(
        lambda row: find_gene_symbol(row['Region Start'], row['Region End'], genes), axis=1
    )
    
    # Save the updated DataFrame either as a new file or overwrite the existing one
    # To save as a new file, change the filename to something like f'updated_transcripts_chr{i}.csv'
    transcripts.to_csv(f'transcripts_chr{i}.csv', index=False)

print("All files have been updated and saved.")
