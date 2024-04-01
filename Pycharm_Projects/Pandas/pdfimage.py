import pytesseract
from pdf2image import convert_from_path


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


def main(pdf_file):
    # Convert PDF to images
    images = pdf_to_images(pdf_file)

    # Extract text from images
    extracted_text = extract_text_from_images(images)

    print(extracted_text)


if __name__ == "__main__":
    pdf_file = r'C:\Users\Sightspectrum\Downloads\64596341 Amendmenttemp0.pdf'  # Replace with your input PDF file
    main(pdf_file)
