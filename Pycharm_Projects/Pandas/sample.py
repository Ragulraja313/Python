import pdfplumber
import pandas as pd
import re

# Replace 'your_file.pdf' with the actual path to your PDF file
pdf_path = r'C:\Users\Sightspectrum\Downloads\WEF_Global_Travel&Tourism_Report_2015.pdf'

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    # Access the specific page
    target_page = pdf.pages[52]  # Page 53 (0-based indexing)

    # Extract text from the target page
    text = target_page.extract_text()

    # Define a regular expression pattern to match the data
    pattern = re.compile(r'(\d+)\s+([^\d]+)\s+([\d.]+)')

    # Find all matches in the text
    matches = pattern.findall(text)

    # Create a DataFrame to store the data
    df = pd.DataFrame(matches, columns=['Rank', 'Economy', 'Value'])

# Convert 'Rank' and 'Value' columns to numeric types
df['Rank'] = pd.to_numeric(df['Rank'])
df['Value'] = pd.to_numeric(df['Value'])


# Remove the first and last rows
df = df.iloc[1:-1]

# Reset index after removing rows
df.reset_index(drop=True, inplace=True)

# Print the DataFrame
print(df)

df.to_excel(r"C:\Users\Sightspectrum\Desktop\sample.xlsx",index=False)