# 数据结构与算法

## 数据结构的存储方式

* 数组：顺序存储
  * 数组由于是紧凑连续存储,可以随机访问，通过索引快速找到对应元素，而且相对节约存储空间。但正因为连续存储，内存空间必须一次性分配够，所以说数组如果要扩容，需要重新分配一块更大的空间，再把数据全部复制过去，时间复杂度 O(N)；而且你如果想在数组中间进行插入和删除，每次必须搬移后面的所有数据以保持连续，时间复杂度 O(N)。
* 链表：链式存储
  * 链表因为元素不连续，而是靠指针指向下一个元素的位置，所以不存在数组的扩容问题；如果知道某一元素的前驱和后驱，操作指针即可删除该元素或者插入新元素，时间复杂度 O(1)。但是正因为存储空间不连续，你无法根据一个索引算出对应元素的地址，所以不能随机访问；而且由于每个元素必须存储指向前后元素位置的指针，会消耗相对更多的储存空间。

## 递归技巧

* 如果当前层对后序的所有层都有约束时，可以通过辅助函数增长参数列表，借助参数传递约束信息。

## 动态规划

### 动态规划思路

* 重叠子问题
* 最优子结构
* 状态转移方程
  * base case
  * 明确状态
  * 明确选择
  * 定义dp数组/函数

### 动态规划通用解法

* 状态转移方程
  * 暴力递归
  * 带有备忘录的递归解法
  * dp 数组的迭代解法
* 压缩状态空间

> 凑零钱问题
> 状态转移方程
> $dp(n)= \begin{cases} -1, & \text {n < 0} \\ 0, & \text {n = 0} \\ min\{dp(n-coin)+1|coin \in coins\}, &\text {n > 0 } \end{cases}$

```python
# 凑零钱问题
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
    return  dp[amount] if dp[amount] != amount + 1 else -1

print(coinChange(coins,15))
```

## 回溯算法

### 回溯算法思路

> DFS算法(深度优先搜索)
> 要点： 路径、选择列表、结束条件

### 回溯算法通用解法

```python
result = []
def backtrack(路径, 选择列表):
    if 满足结束条件:
        result.add(路径)
        return

    for 选择 in 选择列表:
        做选择
        backtrack(路径, 选择列表)
        撤销选择
```

## BFS 算法

### BFS 算法解题思路

> 问题的本质就是让你在一幅「图」中找到从起点 start 到终点 target 的最近距离

* 双向 BFS 优化
  * 能够知道target目标的情况下
  * trick：优先从数据量少的一端搜索

### BFS 算法通用方法

```c++
// 计算从起点 start 到终点 target 的最近距离
int BFS(Node start, Node target) {
    Queue<Node> q; // 核心数据结构
    Set<Node> visited; // 避免走回头路

    q.offer(start); // 将起点加入队列
    visited.add(start);
    int step = 0; // 记录扩散的步数

    while (q not empty) {
        int sz = q.size();
        /* 将当前队列中的所有节点向四周扩散 */
        for (int i = 0; i < sz; i++) {
            Node cur = q.poll();
            /* 划重点：这里判断是否到达终点 */
            if (cur is target)
                return step;
            /* 将 cur 的相邻节点加入队列 */
            for (Node x : cur.adj())
                if (x not in visited) {
                    q.offer(x);
                    visited.add(x);
                }
        }
        /* 划重点：更新步数在这里 */
        step++;
    }
}
```

## 二分查找

```python
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
    mid = left + (right - left)/2
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
  # 因为left == right, right = mid - 1
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
  # 因为left == right, right = mid - 1
  # return mid - 1
  return right
```

## 滑动窗口算法

```python
#滑动窗口算法框架 
def slidingWindow(s:str, t:str):
  need = dict()
  window = dict()
  [need.update({c:0}) for c in t]
  
  left = 0
  right = 0
  valid = 0
  while (right < len(s)):
    # c 是将移入窗口的字符
    c = s[right]
    # 右移窗口
    right += 1
    # 进行窗口内数据的一系列更新
    pass

    while( window needs shrink):
      # d 是将移出窗口的字符 
      d = s[left]
      left += 1
      # 进行窗口内数据的一系列更新 
      pass
```

## 二叉树的遍历

> 重点在于
>
> * 区分节点终止条件
> * 区分处理逻辑应该放在前序、中序、后序中的哪个位置

```c++
/* 二叉树遍历框架 */
void traverse(TreeNode root) {
    // 前序遍历
    traverse(root.left)
    // 中序遍历
    traverse(root.right)
    // 后序遍历
}
```

## 二叉搜索树

### 二叉搜索树思路

```python
# 通用的遍历框架
def bst(root:TreeNode, target:int):
  if root.val == target:
    # 处理过程
    pass
  elif root.val < target:
    bst(root.left, target)
  elif root.val > target:
    bst(root.right, target)
```

### 二叉搜索树增删查改操作

#### 判定合法性

```python
def isValidBST(root: TreeNode):
  return _isValidBST(root, null, null)

def _isValidBST(root: TreeNode, min:TreeNode, max:TreeNode):
  if root == None:
    return True
  if min == None && root.val <= min.val:
    return False
  if max == None && root.val >= max.val:s
    return False
  return _isValidBST(root.left, min, root) && _isValidBST(root.right, root, max)
```

### 查找

```python
def isInBST(root: TreeNode, target: int):
  if root == None:
    return False
  if root.val == target:
    return True
  elif root.val < target:
    return isInBST(root.left, target)
  elif root.val > target:
    return isInBST(root.right, target)
```

### 插入

```python
def insertIntoBST(root: TreeNode, target: int):
  if root == None:
    return new TreeNode(target)
  # if root.val == target:
  #   # 不会插入已经存在的节点
  #   pass
  if root.val < target:
    root.right = insertIntoBST(root.right, target)
  elif root.val > target:
    root.left = insertIntoBST(root.left, target)
```

### 删除一个数

```python
def _getMin(node:TreeNode):
  while node.left:
    node = node.left
  return node

def deleteNode(root:TreeNode, key:int):
  if not root:
    return None
  if root.val = key:
    if not root.left:
      return root.right
    if not root.right:
      return root.left
    minNode = _getMin(root.right)
    # 使用替换值的方式，交换节点
    root.val = minNode.val
    root.right = deleteNode(root.right, minNode.va2020l)
  elif root.val < key:
    root.left = deleteNode(root.left, key)
  elif root.val > key:
    root.right = deleteNode(root.right, key)
  return root 
```
