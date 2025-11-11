map1 = {'A': 1, 'B': 1, 'C': 1}

mapBig = {'A': 1, 'X':1, 'B': 1, 'F': 1, 'M': 2, 'C': 2}


#print(f"is map1 contained in mapBig?: {map1 in mapBig}")
print(map1.keys())
print(mapBig.keys())

#print(map1.keys() in mapBig.keys())

# How can I make sure that my bigMap contains map1?
print(set(map1.keys()).issubset(mapBig.keys()))


word = "Hello"
print(word[0 : 4 + 1])

arr = [1, 2, 3]
stringArr = "".join([str(x)  for x in arr])
print(stringArr, type(stringArr))

per = [[1, 2, 3], [2, 3, 1]]

print([1, 2, 3] == per[0])


target = []
print("target before: ", target)
target = per[1][:]
print(target)