class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def say_hi() -> None:
        pass


p1 = Person("John", 36)

print(p1.name)
print(p1.age)

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print("Woof!")

    def wag_tail(self):
        print("*wagging tail*")
    
    def __str__(self):
        return f"Dog: {self.name}, Breed: {self.breed}"
        
        
santiago = Dog(name="Santiago", breed="Pitbull")
print(santiago)
santiago.wag_tail()

"""
    Classes need a constructor, in python this is called def __init__(self)
    
    ALL METHODS need to have at least the self param defined in the function, even if we're not going to use the actual param inside the method
    
    if we want to have some useful info when printing the whole object, then we need to define the __str__(self) method, so that we return a string with all the useful information
"""