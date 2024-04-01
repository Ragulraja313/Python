from PIL import Image

# Open the image
image = Image.open(r"C:\Users\Sightspectrum\Downloads\img6.jpg")

# Define the coordinates of the region you want to extract (left, top, right, bottom)
left, top, right, bottom = 50, 280, 300, 450

# Crop the image
cropped_image = image.crop((left, top, right, bottom))

# Display the cropped image
cropped_image.show()
