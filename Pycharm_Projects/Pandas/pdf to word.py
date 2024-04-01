from pdf2docx import Converter


def convert_pdf_to_docx(pdf_file, output_docx_file):
    cv = Converter(pdf_file)
    cv.convert(output_docx_file, start=0, end=None)
    cv.close()


if __name__ == "__main__":
    pdf_file = r'C:\Users\Sightspectrum\Downloads\64596341 Amendmenttemp0.pdf' # Replace with your input PDF file
    output_docx_file = r'C:\Users\Sightspectrum\Downloads\64596341 Amendmenttemp0.docx'  # Replace with the desired output Word file

    convert_pdf_to_docx(pdf_file, output_docx_file)
