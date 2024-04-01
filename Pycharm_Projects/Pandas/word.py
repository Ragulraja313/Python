from docx import Document


def read_word_file(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


# Replace 'your_word_file.docx' with the path to your Word file
file_path = r'C:\Users\Sightspectrum\Downloads\Amendment Request Version 92603374temp0.docx'
text = read_word_file(file_path)
print(text)
