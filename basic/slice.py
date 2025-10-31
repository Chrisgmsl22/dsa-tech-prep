a = ("a", "b", "c", "d", "e", "f", "g", "h")
x = slice(2)

print(f"x: {x}")
print(a[x])


example = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Divide this array by half and create two arrays, where the left elements are in one
# And the right elements are in the other one

middle_point = (len(example) / 2).__round__() - 1 # Keep in mind indexes start at 0
left_side = []
for index, value in enumerate(example):
    if index <= middle_point:
        left_side.append(value)

right_side = []
for index, value in enumerate(example):
    if index > middle_point:
        right_side.append(value)


print(f"left: {left_side}")
print(f"right: {right_side}")

#print(example)


second_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
middle_index = len(second_list) // 2


# Divide this array by half and create two arrays, where the left elements are in one
# And the right elements are in the other one
left = second_list[:middle_index]
right = second_list[middle_index:]
print(middle_index)
print(f"Left side: {left}")
print(f"Right side: {right}")

#x = left + right
x = [left + right]
print(x)