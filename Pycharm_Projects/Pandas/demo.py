import pdfplumber
import pandas as pd
import re

# Replace 'your_file.pdf' with the actual path to your PDF file
pdf_path = r'C:\Users\Sightspectrum\Downloads\WEF_Global_Travel&Tourism_Report_2015.pdf'

# Define a regular expression pattern to match the data
pillar_pattern = re.compile(r'Pillar (\d+): (.+)')
data_pattern = re.compile(r'(\d+)\s+([^\d]+)\s+([\d.]+)')

# Create an empty DataFrame to store the data
df_combined = pd.DataFrame(columns=['Pillar', 'Rank', 'Economy', 'Value'])

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    # Loop through pages 43 to 56 (0-based indexing)
    for page_number in range(42, 56):
        # Access the specific page
        target_page = pdf.pages[page_number]

        # Extract text from the target page
        text = target_page.extract_text()

        # Find the Pillar information
        pillar_match = pillar_pattern.search(text)
        if pillar_match:
            current_pillar = pillar_match.group(1)
            pillar_name = pillar_match.group(2)

            # Find all matches in the text
            matches = data_pattern.findall(text)

            # Create a DataFrame for the current page
            df = pd.DataFrame(matches, columns=['Rank', 'Economy', 'Value'])

            # Convert 'Rank' and 'Value' columns to numeric types
            df['Rank'] = pd.to_numeric(df['Rank'])
            df['Value'] = pd.to_numeric(df['Value'])

            # Remove the first and last rows
            df = df.iloc[1:-1]

            # Add the 'Pillar' column
            df['Pillar'] = int(current_pillar)
            df['Pillar_Name'] = pillar_name

            # Append the DataFrame for the current page to the combined DataFrame
            df_combined = pd.concat([df_combined, df], ignore_index=True)

# Reset index after combining data
df_combined.reset_index(drop=True, inplace=True)

# Print the combined DataFrame
print(df_combined)

# Save the combined DataFrame to Excel
df_combined.to_excel(r"C:\Users\Sightspectrum\Desktop\filter.xlsx", index=False)
