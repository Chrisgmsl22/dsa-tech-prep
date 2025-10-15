"""
Function: 
        sequence[start:stop:step]
        
        start: The index at which the slice begins, if omitted, it defaults to the beginning of the sequence 0
        stop: THe index at which the slice ends, if ommited it defaults to the end of the sequence
        step; the incremenet between each index in the slice, if ommited if defaults to 1
"""
my_string = "Hello World"

# Basic slicing
print(f"Basic slicing: {my_string[0:5]}")
print(f"Basic slicing: {my_string[:5]}") # We can omit the start

# Start at index 6 and go up to index 11 (exclusive)
print(f"Middle slicing: {my_string[6:11]}")


print(f"Basic slicing: {my_string[6:]}") # We can omit the end
print(f"Basic slicing: {my_string[6:len(my_string)]}") # We can omit the end


# Slicing the entire sequence
# To create a copy of the entire sequence, you can omit both start and stop
print(f"Create a copy of the entire sequence: {my_string[:]}")


# using step, value allows you to skip characters as you slice
print(f"Slice elements: {my_string[::2]}")


# Start at index 1, go to the end and take every second character
print(f"Slice elements: {my_string[1:len(my_string):2]}")
print(f"Slice elements: {my_string[1::2]}")

# Reversomg a sequence with a negative step
print(f"Reverse a string using slicing: {my_string[0:len(my_string):-1]}")
print(f"Reverse a string using slicing: {my_string[::-1]}")

numbers = [1, 2, 3, 4]
print(f"Slicing an array: {numbers[-1::-1]}")
print(f"Slicing an array: {numbers[:-1][::-1]}")
print(f"Slicing an array: {numbers[::-1]}")

my_list = [10, 20, 30, 40, 50]
print(my_list[1:4])     # Output: [20, 30, 40]
print(my_list[::2])     # Output: [10, 30, 50]
print(my_list[::-1])    # Output: [50, 40, 30, 20, 10]

my_tuple = (1, 2, 3, 4, 5)
print(my_tuple[:3])    # Output: (1, 2, 3)
print(my_tuple[-2:])   # Output: (4, 5)