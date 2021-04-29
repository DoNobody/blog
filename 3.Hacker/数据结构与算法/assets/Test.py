#!/bin/python

from typing import List


coins = [1,2,5]

def coinChange(coins: List, amount: int):
    dp = list()
    for i in range(amount+1):
        dp.append(amount+1)
    dp[0] = 0
    for i in range(len(dp)):
        for coin in coins:
            if i - coin < 0:
                continue
            dp[i] = min(dp[i], dp[i-coin] + 1)
    print([i for i in range(len(dp))])
    print(dp)
    return  dp[amount] if dp[amount] != amount + 1 else -1

print(coinChange(coins,15))


def binarySearch(nums: list, target: int):
  left = 0
  right = len(nums) - 1
  while(left <= right):
    mid = left + (right - left)//2
    if nums[mid] < target:
      left = mid + 1
    elif nums[mid] > target:
      right = mid - 1
    elif nums[mid] == target:
      # 直接返回
      return mid
  # 返回-1
  return -1

def leftBinarySearch(nums:list, target:int):
  left = 0
  right = len(nums) - 1
  while(left <= right):
    mid = left + (right - left)//2
    if nums[mid] < target:
      left = mid + 1
    elif nums[mid] > target:
      right = mid - 1
    elif nums[mid] == target:
      # 锁定左侧边界
      right = mid - 1
  
  # 最后要检查 left 越界的情况
  if (left >= len(nums) or nums[left] != target):
      return -1
  # 因为left = right, right = mid - 1
  # return mid - 1
  return left
      
def rightBinarySearch(nums:list, target:int):
  left = 0
  right = len(nums) - 1
  while(left <= right):
    mid = left + (right - left)//2
    if nums[mid] < target:
      left = mid + 1
    elif nums[mid] > target:
      right = mid - 1
    elif nums[mid] == target:
      # 锁定右侧侧边界
      left = mid + 1
  
  # 最后要检查 left 越界的情况
  if (right < 0 or nums[right] != target):
      return -1
  # 因为left == right, left = mid + 1
  # return mid + 1
  return right

nums = [1,2,3,3,6,7,8,9]
target = 3
print(nums,"target:",target)
print(binarySearch(nums, target))
print(leftBinarySearch(nums, target))
print(rightBinarySearch(nums, target))

def lengthOfLongestSubstring(s:str):
    window = dict()
    [ window.update({c:0}) for c in s]

    right = 0
    left = 0
    res = 0
    resStr = ""
    while(right < len(s)):
        c = s[right]
        right += 1
        window[c] += 1

        while(window[c] > 1):
            d = s[left]
            left += 1
            window[d] -= 1
        if res <= right - left:
            resStr = s[left:right]
            res = right - left
        # res = max(res, right - left)
    print(resStr)
    return res

s = "wqefsdaafefqjndqkwedweds"
print(s)
print(lengthOfLongestSubstring(s))

# 斜着遍历数组

# 遍历上三角
for i in range(4):
  for j in range(0,4 - i):
    l = i + j
    print("    "* l +str(j)+","+str(l))

# 遍历下三角
for i in range(4):
  for j in range(0, 4 - i):
    l = i + j
    print("    "* j + str((l,j)))