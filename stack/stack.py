"""
    How can I create a stack using python code
"""
class Stack:
    def __init__(self):
        self.stack = []
        self.length = len(self.stack)
        
    def peak(self):
        return self.stack[len(self.stack) - 1]
    
    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        top_item = self.stack.pop()
        return top_item
    
    def print_stack(self) -> None:
        print(self.stack)
        
        
        
my_stack = Stack()

my_stack.push("Google")
my_stack.print_stack()

my_stack.push("Udemy")
my_stack.print_stack()

my_stack.push("Discord")
my_stack.print_stack()

print(f"Current top item: {my_stack.peak()}")

print(f"Top element removed: {my_stack.pop()}")

my_stack.print_stack()