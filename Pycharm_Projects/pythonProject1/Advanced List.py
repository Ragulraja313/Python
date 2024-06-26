# List Comprehension
lit = [i for i in range(10) if i % 2 == 0]
print(lit)

# Sorting the List
lt = [12, 55, 34, 46, 21, 45, 39, 66]
a = sorted(lt)
print(a)

lt.sort(reverse=True)
print(lt)


# Filtering the List
def is_even(number):
    return number % 2 == 0


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_numbers = filter(is_even, numbers)

even_numbers_list = list(even_numbers)

print(even_numbers_list)
