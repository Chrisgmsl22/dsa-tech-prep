"""
    A zip() is a built-in python function that combines multiple iterables (lists, tuples, etc)
    element by element 
    Its output is a ZIP OBJ, which looks like a collection of "(), (), ()"
    This ZIP obj is an iterator, so it can easily be turned into a list by using list(zip(...iterables))
    
"""
names = ["Alice", "Bob", "Charlie"]
ages = [55, 30, 15]
cities = ["NYC", "LA", "Chicago"]

combined = list(zip(names, ages, cities))
print(combined)
print("Unzipped combined: ", *combined)

# Sort this combined list by their age
combinedSorted = sorted(combined, key= lambda x : x[1])
print("Combined sorted: ", combinedSorted)

students = {1: ["Alice", 25], 2: ["John", 20], 3: ["Tim", 36]}

# How could I sort the students map by the students age?
sortedStudents = list(sorted(students.items(), key=lambda item: item[1][1]))
print("Sorted students: ", sortedStudents)



# Sort names by the length of the string
sortedNames = sorted(names, key= lambda x : len(x))
print("sortedNames: ", sortedNames)