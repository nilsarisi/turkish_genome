file_paths = []  # To keep track of all created file paths

for i in range(2, 23):  # Starting from 2 to 22
    file_name = f"transcripts_chr{i}.csv"
    # Create an empty CSV file
    with open(file_name, 'w') as file:
        # Optionally, we could write headers or initial content here
        file.write("")  # Writing an empty string just to create the file
    file_paths.append(file_name)

file_paths