# Slicing is for extracting substrings
my_string = "Hello World"
print(f"substring: {my_string[0:3]}")
print(f"last char: {my_string[-3]}")
print(f"reversed string: {my_string[::-1]}")

# Length of a string
length = len(my_string)
print(length)

# Say hello for each letter in the world: Gol
for _ in range(len('Gol')):
    print('HELLO')
    
# lower, upper case
lower_case = "HAMBURGUER".lower()
print(f"Lower case: {lower_case}")
upper_case = "vehicle".upper()
print(f"upper case: {upper_case}")

# strip() is for removing leading/trailing whitespace
print("  H E L L O World          ".strip())

#split(iterable) splitting a string into a list of substring
csv_values = ['one', 'two', 'three']
print("".join(csv_values)) # Join applies to a string, so use: "".join(iterable)

name = 'alexandria is my place'
print(name.split(" ")) # split applies for a string, so use: string.split(denominator)

#Replace(old, new)
phrase = 'We will lose'
print(phrase.replace("lose", 'win'))

# Turn [1, 2, 3] into string
arr = [1, 2, 3]
res = "".join(map(str ,arr))
print(res)


#find(substring), index(substring): Finding the index of a substring
word = 'desk setups are one of my favorite videos'
index = word.find('my')
another_index = word.index("k")
print(f"index found: {index}")
print(f"Another index: {another_index}")

# List comprehension creates new lists based on existing iterables in a concise way
numbers = [1, 2, 3, 4, 5]
# multiply all elements inside the array times 3
res = [x * 2 for x in numbers]
print(f"List comprehension example: {res}")
even_numbers = [x for x in numbers if x % 2 == 0]
print(f"Even numbers: {even_numbers}")


#len: getting the lentgh of a list
print(f"Getting the lentgh of a list: {len(numbers)}")


# apppend(item), Adding an element to the end of a list
print(f"Append: {even_numbers.append(6), even_numbers}")

# Insert(index, item), inserting an element at a specific index
even_numbers.insert(0, 0) # index, item
print(even_numbers)

# extend, adding multiple elements from an iterable to the end of a list
example = (3, 3, 4, 6, 7, 77)
numbers = [5, 5, 5, 5]
numbers.extend(example)
print(f"After expansion: {numbers}")

#pop(index= -1), Removing and returning an element at a given index (defaults to the last)
list_example = [3, 4, 5]
var = list_example.pop(1) # By default, it will remove the last element
print(var)

# Remove(value) removing the first occurence of a specific value
list_example.remove(4 + 1)
print(list_example)

# Get the sum of al elements inside an array
test = [1, 2, 3, 4, 4, 4, 8, 9, 11, 12, 13]

res = 0
for e in test:
    res += e
print(res)
print(sum(test))


# Count: Counting the number of occurences of a value
print(test.count(4))

# Sort: Sorting the list in place
unsorted_list = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Sort List: {unsorted_list.sort(), unsorted_list}")
print(f"reverse Sort List: {unsorted_list.sort(reverse=True), unsorted_list}")

#sorted(key=..., reverse=False), Returns a new sorted list from the iterable
new = sorted(unsorted_list)
print(new)


# Dictionary manipulation
my_dict = {"name": "Alice", "age": 30}
name = my_dict['name']
age = my_dict.get('age')
city = my_dict.get('city', '404')
print(name, age, city)

## Adding/updating key-value pairs
my_dict['city'] = 'London'

print(my_dict.items(), my_dict.keys(), my_dict.values())
print(list(my_dict.keys()))

## pop(key, default): Removing and returning the value associated with a key
print(my_dict.pop('city', '404'))