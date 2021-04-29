package main

func qsort(arr []int, first, last int) {
	flag := first
	left := first
	right := last

	if first >= last {
		return
	}

	for first < last {
		for first < last {
			if arr[last] >= arr[flag] {
				last--
				continue
			}
			arr[last], arr[flag] = arr[flag], arr[last]
			flag = last
			break
		}

		for first < last {
			if arr[first] <= arr[flag] {
				first++
				continue
			}
			arr[first], arr[flag] = arr[flag], arr[first]
			flag = first
			break
		}
	}

	qsort(arr, left, flag-1)
	qsort(arr, flag+1, right)

}
