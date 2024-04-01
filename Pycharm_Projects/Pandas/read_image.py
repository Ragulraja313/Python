import pytesseract
from PIL import Image

# Path to the image file
image_path = r"C:\Users\Sightspectrum\Downloads\img6.jpg"

# Open the image file
image = Image.open(image_path)

# Perform OCR on the image
highlighted_text = pytesseract.image_to_string(image)

# Print the extracted text
print(highlighted_text)

