'''坚持使用测试用例，并cover 100%'''
import unittest
from leetcode_python import Solution


class TestLeetCode(unittest.TestCase):
    '''测试类'''
    # pylint: disable=invalid-name

    def setUp(self) -> None:
        self.solution = Solution()
        return super().setUp()

    def test_three_sum(self):
        '''three_sum'''
        self.assertEqual(self.solution.three_sum([-1, 1]), [])
        self.assertEqual(self.solution.three_sum(
            [-1, 0, 1, 2, -1, 1, 2, -4]), [[-4, 2, 2], [-1, -1, 2], [-1, 0, 1]])

    def test_merge_two_sort_list(self):
        '''merge_two_sort_list'''
        nums1 = [1,2,3,0,0,0]
        nums2 = [2,5,6]
        self.solution.merge_two_sort_list(nums1, len(nums1) - len(nums2), nums2, len(nums2))
        self.assertEqual(nums1, [1,2,2,3,5,6])

        nums1 = [0]
        nums2 = []
        self.solution.merge_two_sort_list(nums1, len(nums1) - len(nums2), nums2, len(nums2))
        self.assertEqual(nums1, [0])

        nums1 = [0]
        nums2 = [1]
        self.solution.merge_two_sort_list(nums1, len(nums1) - len(nums2), nums2, len(nums2))
        self.assertEqual(nums1, [1])
