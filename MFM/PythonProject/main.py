# Sum of the Digits
#T = int(input("Enter the Number: "))
#
# sum1 = 0
# for i in range(T):
#     N = int(input())
#     sum1 += N
# print("Sum of the Digit: ", sum1)

# Armstrong Numbers

# N = int(input("Enter the Number: "))
#
#
# for i in range(1,N+1):
#     i1 = str(i)
#     st = sum(int(s)**3 for s in i1)
#
#     if i == st:
#         print(i)

# Reversing the List and printing the value

# A = int(input("Enter the Number: "))
#
# a = []
# for i in range(A):
#     N = int(input())
#     a.append(N)
#
# for j in a[::-1]:
#     print(j, end=" ")

# Given an N x N matrix, print the elements of the matrix in a wave form row-wise. For the first row, traverse from left to right, for the second row, traverse from right to left, and continue this alternating pattern for the remaining rows.

# rows = int(input("rows: "))
# col = int(input("columns: "))
#
# matrix = []
# print("entries row-wise:")
#
# for i in range(rows):
#     row = []
#     for j in range(col):
#         row.append(int(input()))
#     matrix.append(row)
#
#
# for i in range(rows):
#     for j in range(col):
#         print(matrix[i][j], end=" ")
#     print()
#
#
# result = []
# for i in range(len(matrix)):
#     if i % 2 == 0:
#         result.extend(matrix[i])
#     else:
#         result.extend(reversed(matrix[i]))
#
# print()
# print(" ".join(map(str, result)))

a = int(input("Enter a number: "))
arr = []
for i in range(a):
    N = int(input())
    arr.append(N)

Maximum_Value = max(arr)
Minimum_Value = min(arr)
print(Maximum_Value, Minimum_Value)
print(Maximum_Value + Minimum_Value)



