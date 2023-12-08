package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"

  "github.com/kwsp/gotlib/number"

)

type Node struct {
	name  string
	left  string
	right string
}
type Nav struct {
	directions   []int
	currentIndex int
}

func (nav *Nav) nextDirection() int {
	i := nav.directions[nav.currentIndex]
	nav.currentIndex += 1
	if nav.currentIndex >= len(nav.directions) {
		nav.currentIndex = 0
	}
	return i
}

type Input struct {
	nav   Nav
	nodes map[string][2]string
}

func makeNav(s string) Nav {
	nav := Nav{}
	for _, c := range s {
		switch c {
		case 'L':
			nav.directions = append(nav.directions, 0)
		case 'R':
			nav.directions = append(nav.directions, 1)
		default:
			log.Fatal("Nav not understood", s)
		}
	}
	return nav
}

func loadInput() (Input, error) {
	f, err := os.Open("inp.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	input := Input{nodes: map[string][2]string{}}
	scanner := bufio.NewScanner(f)
	scanner.Scan()
	input.nav = makeNav(scanner.Text())
	scanner.Scan()
	for scanner.Scan() {
		// Handle line parsing here
		line := scanner.Text()
		fields := strings.Fields(line)
		name := fields[0]
		left := fields[2]
		left = left[1 : len(left)-1]
		right := fields[3]
		right = right[:len(right)-1]
		input.nodes[name] = [2]string{left, right}
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}

	return input, err
}

func (input Input) part1(start, end string) int {
	count := 0
	for start != end {
		dir := input.nav.nextDirection()
		//fmt.Println("At", curr, "going", dir)
		start = input.nodes[start][dir]
		count += 1
	}
	return count
}

func (input Input) part2() int {
	// starting nodes all end
	nodes := []string{}
	for node := range input.nodes {
		if node[len(node)-1] == 'A' {
			nodes = append(nodes, node)
		}
	}
	fmt.Println("starting nodes", nodes)

	firstZ := make([]int, len(nodes))

	count := 0
	for true {
		dir := input.nav.nextDirection()
		for i, node := range nodes {
			nodes[i] = input.nodes[node][dir]
		}
		count += 1

		for i, node := range nodes {
			if node[len(node)-1] == 'Z' && firstZ[i] == 0 {
				firstZ[i] = count
			}
		}

		done := true
		for _, v := range firstZ {
			if v == 0 {
				done = false
			}
		}

		if done {
			break
		}
	}
	fmt.Println("N nav", len(input.nav.directions))
	fmt.Println("First Z", firstZ)

	maxVal := len(input.nav.directions)
	for _, z := range firstZ {
		maxVal = max(maxVal, z)
	}

	primes := number.MakePrimes(maxVal + 1)
	primeFactors := map[int]bool{}
	for _, z := range append(firstZ, len(input.nav.directions)) {
		factors := primes.GetPrimeFactors(z)
		for _, factor := range factors {
			primeFactors[factor] = true
		}
	}
	fmt.Println("primeFactors", primeFactors)

	result := 1
	for k := range primeFactors {
		result *= k
	}

	return result
}
func main() {
	inputs, err := loadInput()
	if err != nil {
		fmt.Println(err)
	}

	//fmt.Println("Part1 =", inputs.part1("AAA", "ZZZ"))
	fmt.Println("Part2 =", inputs.part2())
}
