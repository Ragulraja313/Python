import random

n = random.randrange(1, 10)
guess = int(input("Enter any number: "))
while n != guess:
    if guess < n:
        print("Too low")
        guess = int(input("Enter number again: "))
    else:
        print("Too high!")
        guess = int(input("Enter number again: "))
print("you guessed it right!!")
