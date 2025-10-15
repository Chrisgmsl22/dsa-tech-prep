score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"
    
print(f"Your grade is: {grade}")

# For loops, iterate over sequences (lists, tuples, strings, ranges) or other iterable objects

fruits = ["apple", "banana", 'cherry']

## iterable variable
for fruit in fruits:
    print(f"Current fruit: {fruit}")
    
## Explicit range
for i in range(1, 5 + 1):
    print(i)

## List    
for i in [1, 2, 3, 4]:
    print(f"list: {i}")
    

## Weird experiments
for i in list(range(10)):
    print(f"list.range: {i}")
    
    
my_dictionary = {"a": 1, "b": 2, "c": 3}

## need to unpack items in order to access these 2 elements in the loop
for k,v in my_dictionary.items():
    print(f"Key: {k}, Value: {v}")
    
    
## While loops execute a block of code as long as a certain condition is true
counter = 0
while counter < 5:
    print(f"current count is: {counter}")
    counter += 1
    
    
    