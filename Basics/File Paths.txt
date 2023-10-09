# importing os module
import os

# printing current Directory
print(os.getcwd())

# Creating File path
filepath = os.path.join(os.getcwd(), "New Text Document.txt")
print(filepath)

# Checking the file exists?
print(os.path.exists(filepath))

# Printing the directory name and Filename
print(os.path.dirname(filepath))
print(os.path.basename(filepath))

# Checking the filepath is file or Directory
print(os.path.isdir(filepath))
print(os.path.isfile(filepath))

# Printing the Absolute Path:
print(os.path.abspath(filepath))

print(os.path.split(filepath))
