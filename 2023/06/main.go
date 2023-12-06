package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Input struct {
	time     []int
	distance []int
}

func parseLine(line string) []int {
	var res []int
	for _, s := range strings.Fields(strings.Split(line, ":")[1]) {
		v, err := strconv.Atoi(s)
		if err != nil {
			fmt.Println(err)
			break
		}
		res = append(res, v)
	}
	return res
}

func loadInput() (Input, error) {
	f, err := os.Open("inp.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	var input Input
	scanner := bufio.NewScanner(f)
	scanner.Scan()
	line := scanner.Text()
	input.time = parseLine(line)
	scanner.Scan()
	line = scanner.Text()
	input.distance = parseLine(line)

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}

	return input, err
}

func solveWaysToWin(time, distance int) int {
	result := 0

	holdfor := 1
	for ; holdfor < time; holdfor++ {
		remainingTime := time - holdfor
		travelled := remainingTime * holdfor
		if travelled > distance {
			//fmt.Printf("Hold for %v, travel %v\n", holdfor, travelled)
			result += 1
		}
	}
	return result
}

func solveFast(time, distance int) int {
	// Start at holdfor = time / 2
	// Binary search down to find the start point
	// Binary search up to find the end point
	startTime, endTime := 0, 0

	l, r := 0, time/2
	for l < r {
		m := l + (r-l)/2
		travelled := m * (time - m)
		if travelled > distance {
			r = m
		} else {
			l = m + 1
		}
	}
	startTime = l

	l, r = time/2, time
	for l < r {
		m := l + (r-l)/2
		travelled := m * (time - m)
		if travelled > distance {
			l = m + 1
		} else {
			r = m
		}
	}
	endTime = r

	return endTime - startTime
}

func main() {
	input, err := loadInput()
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(input)

	part1 := 1
	for i, d := range input.distance {
		//part1 *= solveWaysToWin(input.time[i], d)
		part1 *= solveFast(input.time[i], d)
	}
	fmt.Println("Part1 =", part1)

	part2 := solveFast(57726992, 291117211762026)
	fmt.Println("Part2 =", part2)
}
