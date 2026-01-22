class Solution:
    def calPoints(self, operations: list[str]) -> int:
        res: list[int] = []
        n = len(operations)

        for i in range(n):
            # We need a structure to check the current character
            currOp = operations[i]

            match currOp:

                case "+":
                    # Sum the previous two scores
                    res.append(res[-1] + res[-2])

                case "D":
                    res.append(res[-1] * 2)

                case "C":
                    # Remove previous score
                    res.pop()
                case _: # Default
                    # We can assume this will be a number
                    res.append(int(currOp))
        
        return sum(res)






""" 
    NOTES:
    - Input: a list of strings (operations).
        Each operation has a different meaning (integer adds x , + sums the previous 2 scores, D multiplies the previous score by 2, C, removes previous score)
    - Output: A number, which represents the sum of the record AFTER all operations have been processed
            Keep in mind that my operations book has at least one element
            For the current number wrapped in a string, we will need to cast it somehow
            for + there will always be at least two previous scores
            for C and D there will always be at least one previous score in the record book


            Brainstorm.
            We need to define an empty array that we will use to manipulate the content
            We could maybe add some sort of switch case (hashMap, if/elses)
            We will iterate linearly and process each element on the go
            Since this will use an array, the valid operations we will do are going to be stack operations (append, pop, and also index accessing for doubling or adding previous elements)

            Once our linear operation is completed, we will return the sum of the array created

""" 