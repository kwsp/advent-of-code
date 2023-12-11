package main

import (
	"bufio"
	"fmt"
	"os"
)

type Input []string
type Pair [2]int

var (
	North Pair = Pair{-1, 0}
	East  Pair = Pair{0, 1}
	South Pair = Pair{1, 0}
	West  Pair = Pair{0, -1}
)

func (c Pair) Add(d Pair) Pair {
	return Pair{c[0] + d[0], c[1] + d[1]}
}

func (c Pair) Negative() Pair {
	return Pair{-c[0], -c[1]}
}

func (c Pair) Equals(d Pair) bool {
	return c[0] == d[0] && c[1] == d[1]
}

var Exits map[byte][2]Pair = map[byte][2]Pair{
	'|': {North, South},
	'-': {East, West},
	'L': {North, East},
	'J': {North, West},
	'7': {South, West},
	'F': {South, East},
}

func loadInput() (Input, error) {
	f, err := os.Open("inp_.txt")
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

	if err = scanner.Err(); err != nil {
		fmt.Println(err)
	}

	return input, err
}

func (inp Input) findStart() Pair {
	for j, line := range inp {
		for i, c := range line {
			if c == 'S' {
				return Pair{j, i}
			}
		}
	}
	return Pair{}
}

type State struct {
	pos, from Pair
}

func (inp Input) currChar(s State) byte {
	return inp[s.pos[0]][s.pos[1]]
}

func (inp Input) moveNext(s State) (State, error) {
	exits := Exits[inp.currChar(s)]
	moveDir := exits[0]
	if s.from.Equals(exits[0]) {
		moveDir = exits[1]
	}
	return State{s.pos.Add(moveDir), moveDir.Negative()}, nil
}

func (inp Input) FirstStep(pos Pair) State {
	J, I := len(inp), len(inp[0])
	j, i := pos[0], pos[1]
	// go north, from south
	if j > 0 {
		c := inp[j-1][i]
		if c == '|' || c == 'F' || c == '7' {
			return State{pos: Pair{j - 1, i}, from: South}
		}
	}
	// go west from east
	if i > 0 {
		c := inp[j][i-1]
		if c == '-' || c == 'F' || c == 'L' {
			return State{pos: Pair{j, i - 1}, from: East}
		}
	}
	// go east from west
	if i < I-1 {
		c := inp[j][i+1]
		if c == '-' || c == '7' || c == 'J' {
			return State{pos: Pair{j, i + 1}, from: West}
		}
	}
	// go south from north
	if j < J-1 {
		c := inp[j+1][i]
		if c == '-' || c == 'F' || c == 'L' {
			return State{pos: Pair{j + 1, i}, from: North}
		}
	}
	return State{}
}

func main() {
	inp, err := loadInput()
	if err != nil {
		fmt.Println(err)
	}

	start := inp.findStart()
	steps := []Pair{start}
	state := inp.FirstStep(start)
	for inp.currChar(state) != 'S' {
		//fmt.Println(state)
		steps = append(steps, state.pos)
		state, err = inp.moveNext(state)
	}
	//fmt.Println(steps)
	//fmt.Println(len(steps)-1)

	part1 := len(steps) / 2
	fmt.Println("Part1 =", part1)

	grid := make([][]rune, len(inp))
	for i, line := range inp {
		grid[i] = make([]rune, len(line))
	}

	for _, step := range steps {
		grid[step[0]][step[1]] = '#'
	}

	//for _, line := range grid {
	//for _, t := range line {
	//if t {
	//fmt.Printf("#")
	//} else {
	//fmt.Printf(".")
	//}
	//}
	//fmt.Printf("\n")
	//}
	//fmt.Println()

	// Horizontal pass
	for j, line := range grid {
		pathcount := 0
		lasti := 0
		for i := len(line) - 1; i >= 0; i-- {
			if line[i] == '#' {
				lasti = i
				break
			} else {
				grid[j][i] = '.'
			}
		}

		for i, c := range line {
			if c == '#' {
				pathcount += 1
				fmt.Printf("#")
			} else if pathcount%2 == 1 && i < lasti {
				fmt.Printf("I")
				grid[j][i] = 'I'
			} else {
				fmt.Printf(".")
				grid[j][i] = '.'
			}
		}
		fmt.Printf("\n")
	}

	//// Vertical pass
	//for i := range grid[0] {
		//pathcount := 0
		//lasti := 0
		//for j := len(grid) - 1; j >= 0; j-- {
			//if grid[j][i] == '#' {
				//lasti = i
				//break
			//} else {
				//grid[j][i] = '.'
			//}
		//}

		//for j := range grid {
			//c := grid[j][i]
			//if c == '#' {
				//pathcount += 1
			//} else if pathcount%2 == 1 && i < lasti {
				//grid[j][i] = 'I'
			//} else {
				//grid[j][i] = '.'
			//}
		//}

	//}

	n_inside := 0
	for _, line := range grid {
		for _, c := range line {
			if c == 'I' {
				n_inside += 1
			}
			fmt.Printf("%c", c)
		}
		fmt.Printf("\n")
	}

	fmt.Println("Part2 =", n_inside)
}
