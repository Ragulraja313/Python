import cv2
import numpy as np
import pytesseract

# Ensure PyTesseract knows the path to Tesseract executable
# Update the path below according to your Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\SightSpectrum\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Load the image
image_path = r"C:\Users\Sightspectrum\Downloads\ilovepdf_pages-to-jpg\Amendment Request Version 92603374temp0_page-0001.jpg"
image = cv2.imread(image_path)

# Convert to HSV color space to detect yellow color
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    # Assuming the largest contour is the highlighted area
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    roi = image[y:y + h, x + w:x + w + 300]

    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    resized_roi = cv2.resize(thresh_roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    processed_roi = cv2.medianBlur(resized_roi, 5)

    text = pytesseract.image_to_string(processed_roi, lang='eng', config='--psm 6')
    print("Extracted Text:", text.strip())
    with open('extracted_text.txt', 'w') as file:
        file.write(text.strip())
else:
    print("No highlighted area detected.")

cv2.imwrite('processed_roi.jpg', processed_roi)

# r"C:\Users\Sightspectrum\Downloads\img6.jpg"
