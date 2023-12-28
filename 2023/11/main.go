package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/kwsp/gotlib/array"
)

type Input []string

func loadInput() (Input, error) {
	f, err := os.Open("inp.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	var input Input
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		// Handle line parsing here
		line := scanner.Text()
		input = append(input, line)
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}

	return input, err
}

func (inp Input) String() string {
	builder := strings.Builder{}
	for _, line := range inp {
		builder.WriteString(line)
		builder.WriteByte('\n')
	}
	return builder.String()
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func part(input Input, emptySize int) int {
	emptySize -= 1

	// Find galaxies
	galaxies := [][2]int{}
	// Find empty rows
	emptyRows := make([]int, len(input))
	// Find empty columns
	emptyCols := make([]int, len(input))
	emptyCols_ := make([]bool, len(input[0]))
	for i := range emptyCols_ {
		emptyCols_[i] = true
	}

	emptyRowsCount := 0
	emptyColsCount := 0

	for j, line := range input {
		emptyRow := true
		for i, c := range line {
			if c == '#' {
				galaxies = append(galaxies, [2]int{j, i})
				emptyRow = false
				emptyCols_[i] = false
			}
		}

		if emptyRow {
			emptyRowsCount++
		}
		emptyRows[j] = emptyRowsCount
	}

	for i, b := range emptyCols_ {
		if b {
			emptyColsCount++
		}
		emptyCols[i] = emptyColsCount
	}

	//fmt.Println("Galaxies", galaxies)
	//fmt.Println("Rows", emptyRows)
	//fmt.Println("Cols", emptyCols)

	// Every pair of galaxies
	distances := array.Array[int]{}
	for i, g1 := range galaxies {
		for j := i + 1; j < len(galaxies); j++ {
			g2 := galaxies[j]

			row1, row2 := g1[0], g2[0]
			if row1 > row2 {
				row1, row2 = row2, row1
			}
			col1, col2 := g1[1], g2[1]
			if col1 > col2 {
				col1, col2 = col2, col1
			}

			dist := row2 - row1 + col2 - col1 +
				emptySize*(emptyRows[row2]-emptyRows[row1]+emptyCols[col2]-emptyCols[col1])
			distances = append(distances, dist)
		}
	}
	return distances.Sum()
}

func main() {
	input, err := loadInput()
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("Part1 =", part(input, 2))
	fmt.Println("Part2 =", part(input, 1000000))
}
