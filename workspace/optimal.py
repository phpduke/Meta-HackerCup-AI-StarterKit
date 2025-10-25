import sys

def solve():
    n = int(sys.stdin.readline())
    arr = list(map(int, sys.stdin.readline().split()))

    # Kadane's Algorithm
    # max_so_far stores the maximum sum found globally
    # current_max stores the maximum sum of a subarray ending at the current position
    
    max_so_far = arr[0]
    current_max = arr[0]

    for i in range(1, n):
        # For the current element arr[i], the maximum sum ending here is either
        # arr[i] itself (starting a new subarray) or arr[i] added to the
        # maximum sum ending at the previous position (extending the subarray).
        current_max = max(arr[i], current_max + arr[i])
        
        # Update the global maximum sum found so far.
        max_so_far = max(max_so_far, current_max)
    
    print(max_so_far)

solve()