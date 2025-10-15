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