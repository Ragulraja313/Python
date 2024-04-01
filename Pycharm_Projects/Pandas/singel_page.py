import pdfplumber

# Replace 'your_file.pdf' with the actual path to your PDF file
pdf_path = r'C:\Users\Sightspectrum\Downloads\WEF_Global_Travel&Tourism_Report_2015.pdf'

# Specify the page number you want to read (e.g., page 2)
target_page_number = 43

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    # Access the specific page
    target_page = pdf.pages[target_page_number - 1]  

    # Extract text from the target page
    text = target_page.extract_text()

    # Print the text from the target page
    print(f"Page {target_page_number}:\n{text}\n")
