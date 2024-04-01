import pdfplumber


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    print(text)
    return text


def save_text_to_file(text, output_text_file):
    with open(output_text_file, 'w') as file:
        file.write(text)


if __name__ == "__main__":
    pdf_file = r'C:\Users\Sightspectrum\Downloads\Amendment Request Version 92603374temp0 (1).pdf'  # Replace with your input PDF file
    output_text_file = 'output_text_file.txt'  # Replace with the desired output text file

    extracted_text = extract_text_from_pdf(pdf_file)
    save_text_to_file(extracted_text, output_text_file)
