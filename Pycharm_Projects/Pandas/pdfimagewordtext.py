import pytesseract
from pdf2image import convert_from_path
from docx import Document


def pdf_to_images(pdf_file):
    # Convert PDF to images
    images = convert_from_path(pdf_file)
    return images


def extract_text_from_images(images):
    # Extract text from images using OCR
    extracted_text = ''
    for img in images:
        text = pytesseract.image_to_string(img)
        extracted_text += text + '\n'
    return extracted_text


def write_text_to_word(text, output_word_file):
    # Write text to a Word file
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_word_file)


def write_text_to_text_file(text, output_text_file):
    # Write text to a text file
    with open(output_text_file, 'w') as file:
        file.write(text)


def main(pdf_file, output_word_file, output_text_file):
    # Convert PDF to images
    images = pdf_to_images(pdf_file)

    # Extract text from images
    extracted_text = extract_text_from_images(images)

    # Write extracted text to Word file
    write_text_to_word(extracted_text, output_word_file)

    # Write extracted text to text file
    write_text_to_text_file(extracted_text, output_text_file)


if __name__ == "__main__":
    pdf_file = r'C:\Users\Sightspectrum\Desktop\Project\Pandas\Amendment Request Version 92603374temp0.pdf'  # Replace with your input PDF file
    output_word_file = r'C:\Users\Sightspectrum\Desktop\Project\Pandas\Amendment Request Version 92603374temp0.docx'  # Replace with the desired output Word file
    output_text_file = 'output_text_file.txt'  # Replace with the desired output text file

    main(pdf_file, output_word_file, output_text_file)
