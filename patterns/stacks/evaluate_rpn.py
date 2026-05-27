"""
You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.

Note that:

The valid operators are '+', '-', '*', and '/'.
Each operand may be an integer or another expression.
The division between two integers always truncates toward zero.
There will not be any division by zero.
The input represents a valid arithmetic expression in a reverse polish notation.
The answer and all the intermediate calculations can be represented in a 32-bit integer.
 

Example 1:

Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9
Example 2:

Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6
Example 3:

Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22




""" 


class Solution:
    def _isNum(self, num: str) -> bool:
        try:
            int(num)
            return True
        except ValueError:
            return False
    def evalRPN(self, tokens: list[str]) -> int:
        res = []
        i = 0
        calculate = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a // b
        }
        # might need to skip...
        # ["2","1","+","3","*"]
        #          i
        # [2, 1]
        while i < len(tokens):
            currToken = tokens[i]
            print("Current TOKEN: ", currToken)

            # If token is a number, append to queue
            if self._isNum(currToken):
                print("adding: ", currToken)
                res.append(int(currToken))
            else: 
                #print("res before pops: ", res, "curr token: ", currToken)
                rightNum = res.pop()
                leftNum = res.pop()
                operation = calculate[currToken](leftNum, rightNum)
                print(f"{leftNum} {currToken} {rightNum} = {operation}")
                res.append(operation)

            # If token is not a number, pop 2 from queue and perform operation 
            i += 1
        print("res after all operations: ", res)
        return res[-1]



sol = Solution()

tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]

res = sol.evalRPN(tokens)
print(res)

""""
    NOTES:
    - Input, an array of strings, it can contain a valid operator and an integer from the range -200 to 200
    - Output: Integer, which represents the result of the operation by readin the reverse polish notation.
    - Assumptions: There will always be valid operators, division between two integers always truncates toward zero (// ?), there will not be a division by zero.
    Input represents a valid arithmetic expression in a reverse polish notation

    In a reverse polish notation the OPERATORS (+-*/) are after their OPERANDS (12345)

     (3 + 4) × (5 + 6) becomes 3 4 + 5 6 + × in reverse Polish notation.

     "The concept of a stack, a last-in/first-out construct, is integral to the left-to-right evaluation of RPN. In the example 3 4 −, first the 3 is put onto the stack, then the 4; the 4 is now on top and the 3 below it. The subtraction operator removes the top two items from the stack, performs 3 − 4, and puts the result of −1 onto the stack."


     Initial approach:
     This mathematical notation seems to be using a stack for effectiveness. The goal of this notation is to remove parentheses when it comes to developing an expression. So instead of doing 1 + 2 = 3, 
     we do 1 2 +

     (1 + 1) / (2 * 1) would be ... ==> 11+ 21* / 

     Based on the wikipedia file, we will be using a stack to process this logic.
     We will go from left to right, we append numbers as we see them, and as soon as we see an operator,
     we pop the last 2 elements and push the operation made by looking at the current operator.


"""