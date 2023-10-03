# Opening the File
f = open("C:\\Users\\SightSpectrum\\Desktop\\New Text Document.txt", "r")

# Reading and Printing the File
print(f.read())
f.close()

# Printing the First Line
f = open("C:\\Users\\SightSpectrum\\Desktop\\New Text Document.txt", "r")
print(f.readline())
f.close()

# Printing the Specific Part
f = open("C:\\Users\\SightSpectrum\\Desktop\\New Text Document.txt", "r")
print(f.read(8))

# Printing the text in List
print(f.readlines())
f.close()


# Writing the File
# Appending the Text File
f = open("C:\\Users\\SightSpectrum\\Desktop\\New Text Document.txt", "a")
f.write("\nHi Everyone!!!")
f.close()

f = open("C:\\Users\\SightSpectrum\\Desktop\\New Text Document.txt", "r")
print(f.read())
f.close()

# Rewriting the Whole Content
f = open("C:\\Users\\SightSpectrum\\Desktop\\New Text Document.txt", "w")
f.write("Hi Everyone!!!")
f.close()

f = open("C:\\Users\\SightSpectrum\\Desktop\\New Text Document.txt", "r")
print(f.read())