'''Leetcode practice case'''


class Solution:
    '''Leetcode 模板'''
    # pylint: disable=invalid-name
    # pylint: disable=line-too-long

    def three_sum(self, nums: list[int]) -> list[list[int]]:
        '''
            给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，
        同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。
            注意：答案中不可以包含重复的三元组。
            示例 1：
                输入：nums = [-1,0,1,2,-1,-4]
                输出：[[-1,-1,2],[-1,0,1]]
                解释：
                nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
                nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
                nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
                不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
                注意，输出的顺序和三元组的顺序并不重要。
        解法：
            list 排序
            list 循环选择
            左右两个数字逼近
        '''
        nums_lens = len(nums)

        if (not nums or nums_lens < 3):
            return []

        nums.sort()
        res: list[list[int]] = []

        for i in range(nums_lens):
            if nums[i] > 0:
                break
            if (i > 0 and nums[i] == nums[i-1]):
                continue

            L = i+1
            R = nums_lens-1
            while L < R:
                if nums[i] + nums[L] + nums[R] == 0:
                    sort_list = [nums[L], nums[i], nums[R]]
                    sort_list.sort()
                    res.append(sort_list)
                    while (L < R and nums[L] == nums[L+1]):
                        L = L+1
                    while (L < R and nums[R] == nums[R-1]):
                        R = R - 1
                    L = L + 1
                    R = R - 1
                elif nums[i] + nums[L] + nums[R] > 0:
                    R = R - 1
                else:
                    L = L + 1
        return res

    def merge_two_sort_list(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        给你两个按 非递减顺序 排列的整数数组 nums1 和 nums2，另有两个整数 m 和 n ，分别表示 nums1 和 nums2 中的元素数目。
        请你 合并 nums2 到 nums1 中，使合并后的数组同样按 非递减顺序 排列。
        注意：最终，合并后数组不应由函数返回，而是存储在数组 nums1 中。为了应对这种情况，nums1 的初始长度为 m + n，其中前 m 个元素表示应合并的元素，后 n 个元素为 0 ，应忽略。nums2 的长度为 n 。

            示例 1：

            输入：nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
            输出：[1,2,2,3,5,6]
            解释：需要合并 [1,2,3] 和 [2,5,6] 。
            合并结果是 [1,2,2,3,5,6] ，其中斜体加粗标注的为 nums1 中的元素。
            示例 2：

            输入：nums1 = [1], m = 1, nums2 = [], n = 0
            输出：[1]
            解释：需要合并 [1] 和 [] 。
            合并结果是 [1] 。
            示例 3：

            输入：nums1 = [0], m = 0, nums2 = [1], n = 1
            输出：[1]
            解释：需要合并的数组是 [] 和 [1] 。
            合并结果是 [1] 。
            注意，因为 m = 0 ，所以 nums1 中没有元素。nums1 中仅存的 0 仅仅是为了确保合并结果可以顺利存放到 nums1 中。
        解:
            把正确的数放在正确的位置上。
            可以从数分析，也可以从位置分析
            发现在位置上放数比较方便

        """

        k = m + n - 1

        while m > 0 and n > 0:
            if nums1[m - 1] > nums2[n - 1]:
                nums1[k] = nums1[m - 1]
                m -= 1
            else:
                nums1[k] = nums2[n - 1]
                n -= 1
            k -= 1
        nums1[:n] = nums2[:n]


    def remove_element(self, nums: list[int], val: int) -> int:
        """
        给了一个数组，和一个倒数，从数组中删除这一倒数，返回新数组的长心
        """
        nums_len = len(nums)
        if not nums_len:
            return 0
        i = 0
        while i < nums_len:
            if nums[i] == val:
                nums.pop(i)
                nums_len -= 1
            else:
                i += 1
        return nums_len
