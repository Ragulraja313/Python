def check(a, b):
    if sorted(a) == sorted(b):
        print("The strings are anagrams.")
    else:
        print("The strings aren't anagrams.")

    # driver code


a = "listen"
b = "silent"
check(a, b)
