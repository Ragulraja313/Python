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


class Employee(Human):
    pass


e = Employee("Sonia", 20)
e.display()


# Single inheritance
class Fun:

    def __init__(self, name):
        self.name = name
        print(f"My name is {self.name}")


class Fun1(Fun):
    print("Hi! Hello How U do!")


s = Fun("Ajeeth")
s1 = Fun1("Snegha")

print(s.name)
print(s1.name)


# Multiple Inheritance
class Mother:
    mothername = ""

    def mother(self):
        print(self.mothername)


class Father:
    fathername = ""

    def father(self):
        print(self.fathername)


class Son(Mother, Father):
    def parents(self):
        print("Father :", self.fathername)
        print("Mother :", self.mothername)


s1 = Son()
s1.fathername = "RAM"
s1.mothername = "SITA"
s1.parents()


# Multilevel inheritance
class Grandfather:

    def __init__(self, grandfathername):
        self.grandfathername = grandfathername


class Father(Grandfather):
    def __init__(self, fathername, grandfathername):
        self.fathername = fathername

        # invoking constructor of Grandfather class
        Grandfather.__init__(self, grandfathername)


class Son(Father):
    def __init__(self, sonname, fathername, grandfathername):
        self.sonname = sonname

        # invoking constructor of Father class
        Father.__init__(self, fathername, grandfathername)

    def print_name(self):
        print('Grandfather name :', self.grandfathername)
        print("Father name :", self.fathername)
        print("Son name :", self.sonname)


s1 = Son('Prince', 'Ramp', 'Lal mani')
print(s1.grandfathername)
s1.print_name()


# Hierarchical inheritance
class Parent:
    def func1(self):
        print("This function is in parent class.")


class Child1(Parent):
    def func2(self):
        print("This function is in child 1.")


class Child2(Parent):
    def func3(self):
        print("This function is in child 2.")


object1 = Child1()
object2 = Child2()
object1.func1()
object1.func2()
object2.func1()
object2.func3()


# Hybrid inheritance
class School:
    def func1(self):
        print("This function is in school.")


class Student1(School):
    def func2(self):
        print("This function is in student 1. ")


class Student2(School):
    def func3(self):
        print("This function is in student 2.")


class Student3(Student1, School):
    def func4(self):
        print("This function is in student 3.")


object = Student3()
object.func1()
object.func2()
