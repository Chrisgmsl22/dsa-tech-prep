def power(x, n):
    # Base case
    if n == 0: return 1
    if n == 1: return x
    
    return x * power(x, n - 1)

# Test: power(2, 5) should return 32

print(power(     5))