package main

import (
	"fmt"
)

func lengthOfLongestSubstring(s string) int {
	// 无重复字符的最长子串
	left := 0
	right := 0
	res := 0
	window := make(map[string]int, len(s))
	if len(s) == 0 {
		return 0
	}

	for ; right != len(s); right++ {
		c := s[right : right+1]
		if _, ok := window[c]; ok == false {
			window[c] = 1
		} else {
			window[c]++
		}

		for ; window[c] > 1; left++ {
			d := s[left : left+1]
			window[d]--
		}
		if res <= right-left {
			res = right - left
		}

	}
	return res + 1
}

func main() {
	// 无重复字符的最长子串
	fmt.Println(lengthOfLongestSubstring("wqefsdaafefqjndqkwedweds"))
}
