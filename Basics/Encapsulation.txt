# Public
class Human:
    Name = ""
    Age = 0

    def __init__(self, Name, Age):
        self.name = Name
        self.age = Age

    def display(self):
        print(f"My name is {self.name} and age is {self.age}")


s = Human("Rahul", 22)
print(s.name)
print(s.age)
s.display()


# Protected
class Human1:
    name = None
    age = None

    def __init__(self, name, age):
        self._name = name
        self._age = age

    def _display(self):
        print(f"{self._name} is {self._age}")


class Rahul(Human1):

    def display(self):
        print(self._name)
        print(self._age)
        self._display()


r = Rahul("Raja", 23)
r.display()


# Private
class Human2:
    __firstname = None
    __lastname = None

    def __init__(self, firstname, lastname):
        self.__firstname = firstname
        self.__lastname = lastname

    def __display(self):
        print(self.__firstname + self.__lastname)

    def dis(self):
        Human2.__display(self)


e = Human2("Max", "Morphin")
e.dis()
