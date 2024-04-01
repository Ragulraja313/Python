from docx import Document


def read_word_file(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def write_text_to_file(text, output_file):
    with open(output_file, 'w') as file:
        file.write(text)


if __name__ == "__main__":
    word_file = r'C:\Users\Sightspectrum\Downloads\Amendment Request Version 92603374temp0 (1).docx'  # Replace with your input Word file
    output_text_file = 'output_text_file.txt'  # Replace with the desired output text file

    word_text = read_word_file(word_file)
    write_text_to_file(word_text, output_text_file)
