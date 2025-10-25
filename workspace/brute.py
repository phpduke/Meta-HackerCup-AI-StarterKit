n = int(input())
arr = list(map(int, input().split()))

max_so_far = float('-inf')

for i in range(n):
    current_sum = 0
    for j in range(i, n):
        current_sum += arr[j]
        max_so_far = max(max_so_far, current_sum)

print(max_so_far)