package array

type Array[T int | int64 | float64] []T

// Diff returns the diff array and a bool indicating if
// all values in the diff array are zeros
func (arr Array[T]) Diff() (Array[T], bool) {
	diff := []T{}
	n := len(arr)
	allZeros := true
	for i := 1; i < n; i++ {
		diff_i := arr[i] - arr[i-1]
		if diff_i != 0 {
			allZeros = false
		}
		diff = append(diff, diff_i)
	}
	return diff, allZeros
}

// Returns the first value
func (arr Array[T]) First() T {
	return arr[0]
}

// Returns the last value
func (arr Array[T]) Last() T {
	return arr[len(arr)-1]
}

func (arr Array[T]) Reversed() Array[T] {
	reversed := make(Array[T], len(arr))
	n := len(arr)
	for i := 0; i < n; i++ {
		reversed[n-i-1] = arr[i]
	}
	return reversed
}
