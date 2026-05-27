import heapq


# Lets create a min heap, it will just be a list
heap = []

# Add elements O(log n)
heapq.heappush(heap, 5)
heapq.heappush(heap, 3)
heapq.heappush(heap, 7)
heapq.heappush(heap, 1)


print("heap after pushes: ", heap)

# Get the minimum value O(1)
print(heap[0])

# Remove and get the minimum element O(log n)
minVal = heapq.heappop(heap)
print("Removed smallest element and re arranged existing heap ", minVal)
print(heap)


# We can also build a heap from an existing list O(n)
nums = [5, 2, 8, 1, 9]

heapq.heapify(nums)
print("Nums turned into a heap: ", nums)


"""
    Python's built in library only contains a min heap
    If we want to deal with a max heap, we can use a min heap and just negate the value
"""

arr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

print("Original arr: ", arr)

# Turn arr into a heap
heapq.heapify(arr)

print("arr turned into a min heap: ", arr)

maxHeap = []
for num in arr:
    heapq.heappush(maxHeap, -num)

print("minHeap turned into max: ", maxHeap)

print("max: ", -maxHeap[0])