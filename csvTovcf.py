import pandas as pd

# Using a raw string for the path to avoid issues with backslashes
df = pd.read_csv(r"combined_chr1_to_chr22_last.csv")

# Define a function to convert rows to VCF format (this is a placeholder, adjust based on your actual data columns)
def format_vcf_row(row):
    info_fields = [
        f"AF={row['Allele Frequency']}", 
        f"AC={row['Allele Count']}",
        f"AN={row['Allele Number']}",
        f"POS={row['Position']}",
        "DP=100"  # Depth of Coverage (example value)
    ]
    info = ";".join(info_fields)
    # Return the formatted VCF line (example format)
    return f"{row['chromosome']}\t{row['Position']}\t.\tREF\tALT\t.\t.\t{info}"

# Apply the format function to each row and create a new column for VCF formatted data
df['VCF_Format'] = df.apply(format_vcf_row, axis=1)

# Write the VCF output to a file
with open('output.vcf', 'w') as file:
    # Writing a simple header for the VCF file
    file.write("##fileformat=VCFv4.2\n")
    file.write("#CHROM POS ID REF ALT QUAL FILTER INFO\n")
    for line in df['VCF_Format']:
        file.write(line + "\n")

print("VCF file created successfully!")
