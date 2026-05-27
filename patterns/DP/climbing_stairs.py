"""
You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

"""
class Solution:
    def climbStairs(self, n: int) -> int:
        
        def F(num: int) -> int:
            if num <= 1:
                return num

            return F(num - 1) + F(num - 2)
        
        return F(n + 1)



sol = Solution()

n = 44

print("Final result: ", sol.climbStairs(n))

"""
    WE CAN ONLY JUMP 1 OR 2 STEPS

    If it takes me N steps to reach the top, then n is 2

    it takes me 2 steps to reach the top

    How many ways can we climb to the top?


    n = 1 ==> then only 1 
    n = 2 ==> 2 (1 + 1)(2) 2
    n = 3 ==> (1 1 1 )(1 2)(2 1) 3
    n = 4 ==> (1111)(121)(112)(211)(22) 5
    n = 5 ==> (11111)(1211)(1121)(1112)(2111)(122)(221)(212) 8

"""