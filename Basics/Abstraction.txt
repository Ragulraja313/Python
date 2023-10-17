from abc import ABC, abstractmethod


class Raja(ABC):
    @abstractmethod
    def display(self):
        pass


class Raja1(Raja):
    def display(self):
        print("Hello")


class Raja2(Raja1):
    def display(self):
        print("Hello")


raja1 = Raja1()
raja2 = Raja2()
raja1.display()
raja2.display()
