# create a class
class Room:
    length = 0.0    # Giving Attributes
    breadth = 0.0

    # method to calculate area
    def area(self):
        print(self.length * self.breadth)


# create object of Room class
rom = Room()


# assign values to all the attributes 
rom.length = 42.5
rom.breadth = 30.8


# access method inside class
rom.area()