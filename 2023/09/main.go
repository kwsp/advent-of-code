package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Input []int
type Inputs []Input

func parseLine(line string) (Input, error) {
	inp := Input{}
	for _, val := range strings.Fields(line) {
		x, err := strconv.Atoi(val)
		if err != nil {
			return inp, err
		}
		inp = append(inp, x)
	}
	return inp, nil
}

func loadInput() (Inputs, error) {
	f, err := os.Open("inp.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	inputs := Inputs{}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		// Handle line parsing here
		line := scanner.Text()
		inp, err := parseLine(line)
		if err != nil {
			fmt.Println(err)
			break
		}
		inputs = append(inputs, inp)
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}

	return inputs, err
}

// returns the diff array and if all values in the
// diff array are all zeros
func (inp Input) getDiff() (Input, bool) {
	diff := []int{}
	n := len(inp)
	isAllZeros := true
	for i := 1; i < n; i++ {
		diff_i := inp[i] - inp[i-1]
		if diff_i != 0 {
			isAllZeros = false
		}
		diff = append(diff, diff_i)
	}
	return diff, isAllZeros
}

func (arr Input) last() int {
	return arr[len(arr)-1]
}

func (arr Inputs) part1() int {
	results := 0
	for _, inp := range arr {
		// Layers of diffs
		layers := Inputs{inp}
		for true {
			diff, allZeros := layers[len(layers)-1].getDiff()
			if allZeros {
				break
			}
			layers = append(layers, diff)
		}
		//fmt.Println(layers)

		// Add new elements
		nLayers := len(layers)
		for i := nLayers - 2; i >= 0; i-- {
			layer := &layers[i]
			diff := &layers[i+1]
			*layer = append(*layer, layer.last()+diff.last())
		}
		//fmt.Println(layers)
		//fmt.Println()
		results += layers[0].last()
	}
	return results
}

func (arr Input) Reversed() Input {
	reversed := make(Input, len(arr))
	n := len(arr)
	for i := 0; i < n; i++ {
		reversed[n-i-1] = arr[i]
	}
	return reversed
}

func main() {
	inputs, err := loadInput()
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("Part1 =", inputs.part1())
	inputsReversed := make(Inputs, len(inputs))
	for i, inp := range inputs {
		inputsReversed[i] = inp.Reversed()
	}
	fmt.Println("Part2 =", inputsReversed.part1())
}
