# Variables have dynamic type, the interpreter infers the type at runtime based on the value assigned

name = "Alice"
age = 39
is_student = False
price = 99.99

# Python uses snake_case convention (do not use camelCase for this language)

# Data types

#int
integer_var = -5

#float
float_var = 3.14

#complex 
complex_var = 3 + 5j

#string
string_var = "Hello World"

#Boolean
bool_var = True

"""
    Sequence Type:
    - Lists: Ordered, mutable collection of items, enclosed in square brackts [], it can contain multiple items
"""
my_list = [1, "hello", 3.14, True]
my_list[0] = 10 # Lists are mutable
print(f"This is my list: {my_list}")

""""
    Tuples:
    Ordered, immutable collection of items, these are enclosed in parenthesis
"""
my_tuple = (1, "Hello", 3.14, True)
print(f"This is my tuple: {my_tuple}")

"""
    Range:
    Represents an immutable sequence of numbers, these are often used for looping
"""
numbers = range(5) # Represents 0, 1, 2, 3, 4
print(f"This is my range of numbers: {numbers}")

# if you want to display the actual numbers in the range, we need to explicitly convert the range object to a list using list
converted = list(numbers)
print(converted)
print(list(range(0, 100 + 1)))

"""
    Sets:
    Unordered collection of UNIQUE ITEMS, enclosed in {}
    (DUPLICATES ARE REMOVED)
"""
my_set = {1, 2, 2, 3, 4, 4}
print(f"This is my set: {my_set}")

my_list = [1, 2, 2, 3, 4, 4]
print(my_list)
print(set(my_list))
print(tuple(my_list))

"""
    Dictionary:
    Unordered collection of key-value pairs, Keys must be unique and immutable, enclosed in {} with colons : separating keys and values
"""
my_dict = {"name": "Charlie", "age": 25, "city": "New York", "name": "ron"}
second_dict = {1: "one", 1: "two", 3: "three"}
print(f"Printing the whole obj: {my_dict}")
print(f"Printing the whole obj: {second_dict}")
print(my_dict["name"])

custom_var = None