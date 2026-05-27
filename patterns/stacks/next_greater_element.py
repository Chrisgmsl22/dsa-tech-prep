class Solution:
    def nextGreaterElementBRUTE(self, nums1: list[int], nums2: list[int]) -> list[int]:
        n = len(nums1)
        n2 = len(nums2)
        res = [-1] * n # nums1 size is going to be the res.

        for i in range(n):
            # find current number
            currNum = nums1[i]
            currNumIdx = nums2.index(currNum)
            print(currNumIdx)

            while currNumIdx < n2:
                if nums2[currNumIdx] > currNum: # Then we set this in the list
                    print("idx: ", i)
                    res[i] = nums2[currNumIdx]
                    break
                currNumIdx += 1
        return res
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        n2 = len(nums2)
        res = []
        stack = []
        hashMap: dict[int, int] = {}

        for i in range(n2):
            currNumber = nums2[i]

            # n1 = [4, 1, 2]
            # n2 = [1, 3, 4, 2]
            #          i
            # stack = [1, ]
            while stack and currNumber > stack[-1]:
                # pop and process
                topVal = stack.pop()
                hashMap[topVal] = currNumber # CurrNumber is going to be the next greater element
            stack.append(currNumber)

        print(hashMap)
        # Now we go over our answer.
        for num in nums1:
            res.append(hashMap.get(num, -1))
        
        return res


sol = Solution()
nums1 = [4,1,2] 
nums2 = [1,3,4,2]

res = sol.nextGreaterElement(nums1, nums2)
print(res)

"""
    NOTES:
    - Input: two integer arrays, where arr1 is a subset of arr2 (subset means that arr1's elements are contained within arr2)
    - Ouput: An array, which contains the next greater element for the elements of arr1 (element, not index).
    If there is not a greater element, then we set the value to -1

    Assumptions: Do these 2 arrays contain values?. does arr1 need to be smaller than arr2?, elements cannot be repeated
    numbers in arr1 must be contained within arr2

    We need to keep track of their indices. We will take arr1 as our starting point.
    We also need to define the result, which we can have an array with a fixed length of len(arr1) and -1 as the default values

    We need to find our current number in arr2, since numbers may not be sorted, we simply iterate over the array until we find the number.
    Once we find it, we see if there is any other greater element in the array, if it is, we set the very next greater element and break iterations (does not matter if there are bigger numbers, this problem asks us for the next one)


"""