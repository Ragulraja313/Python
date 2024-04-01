import csv

with open(r"C:\Users\SightSpectrum\Desktop\Input.csv", "r") as file:
    data = csv.reader(file)

    for i in data:
        print(i)

with open("C:\\Users\\SightSpectrum\\Desktop\\Input.csv", "a") as file:
    data = csv.writer(file)
    fields = ['Name', 'Branch', 'Year', 'CGPA']

    a = [['Nikhil', 'COE', '2', '9.0'],
         ['Sanchit', 'COE', '2', '9.1'],
         ['Aditya', 'IT', '2', '9.3'],
         ['Sagar', 'SE', '1', '9.5'],
         ['Prateek', 'MCE', '3', '7.8'],
         ['Sahil', 'EP', '2', '9.1']]

    data.writerow(fields)
    data.writerows(a)







