"""
    Problem 3: Print Numbers 1 to N

Given n, print numbers from 1 to n (in order).

Hint:

Base case → stop at 1.

Think carefully: do you recurse before or after the print to get the right order?
"""
class Recursion:
    def printNums(self, num: int, starter = 1) -> None:
        # Identify base case
        print(starter)
        if num == starter:
            return
        
        # Identify recursion case
        return self.printNums(num, starter + 1)
    
    def printNums2(self, n: int) -> None: 
        if n <= 0:
            return
        
        self.printNums2(n - 1)
        print(n)
    

inputData = 10
problem = Recursion()

problem.printNums2(inputData)
