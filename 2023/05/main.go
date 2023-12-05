package main

import (
	"bufio"
	"errors"
	"fmt"
	"github.com/schollz/progressbar/v3"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Range struct {
	sstart int
	dstart int
	n      int
}

func (r Range) v_lt(v int) bool { return v < r.sstart }
func (r Range) v_gt(v int) bool { return r.sstart+r.n <= v }
func (r Range) v_in(v int) bool { return r.sstart < v && v < r.sstart+r.n }

type Group []Range

func (g Group) Len() int           { return len(g) }
func (g Group) Swap(i, j int)      { g[i], g[j] = g[j], g[i] }
func (g Group) Less(i, j int) bool { return g[i].sstart < g[j].sstart }

type Input struct {
	seeds  []int
	groups []Group
}

func parseLine(line string) (Input, error) {
	//lineparts := strings.Split(line, " ")

	var err error
	inp := Input{}
	return inp, err
}

func Str2Ints(line string) ([]int, error) {
	vals := []int{}
	var err error
	for _, word := range strings.Split(line, " ") {
		num, err := strconv.Atoi(word)
		if err != nil {
			fmt.Println(err)
			break
		}
		vals = append(vals, num)
	}
	return vals, err
}

func ParseRange(line string) (Range, error) {
	vals, err := Str2Ints(line)
	if err != nil {
		return Range{}, err
	}
	if len(vals) != 3 {
		return Range{}, errors.New("Wrong number of values")
	}
	return Range{sstart: vals[1], dstart: vals[0], n: vals[2]}, err
}

func loadInput() (Input, error) {
	f, err := os.Open("inp.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	scanner.Scan()
	line := scanner.Text()

	// First line is seeds
	line = strings.SplitN(line, ": ", 2)[1]
	seeds, err := Str2Ints(line)
	if err != nil {
		fmt.Println(err)
	}
	//fmt.Println("Parsed seeds", seeds)

	scanner.Scan() // Read an empty line (discard)
	scanner.Scan() // Read group header (discard)

	groups := []Group{}
	group := Group{}
	for scanner.Scan() {
		line = scanner.Text()

		if len(line) == 0 {
			// Finished a group
			sort.Sort(group)
			groups = append(groups, group)
			group = Group{}

			scanner.Scan() // Discard next header
		} else {
			r, err := ParseRange(line)
			if err != nil {
				fmt.Println(err)
				break
			}
			group = append(group, r)
		}
	}
	sort.Sort(group)
	groups = append(groups, group)

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}

	return Input{seeds: seeds, groups: groups}, err
}

func query(ranges Group, v int) int {
	l, r := 0, len(ranges)
	m := 0
	for l < r {
		m = l + (r-l)/2
		curr := ranges[m]
		if curr.v_lt(v) {
			r = m
		} else if curr.v_gt(v) {
			l = m + 1
		} else {
			// curr.v_in(v) must be true
			return v - curr.sstart + curr.dstart
		}
	}
	return v
}

func queryAll(groups []Group, v int) int {
	for _, g := range groups {
		v = query(g, v)
	}
	return v
}

func (inp Input) Part1() int {
	res := math.MaxInt
	for _, seed := range inp.seeds {
		v := queryAll(inp.groups, seed)
		res = min(res, v)
	}
	return res
}

func (inp Input) Part2() int {
	res := math.MaxInt
	n_seeds := 0
	for i := range inp.seeds {
		if i%2 == 0 {
			//seed_start := inp.seeds[i]
			n_rep := inp.seeds[i+1]
			n_seeds += n_rep
		}
	}
	fmt.Println(`n_seeds =`, n_seeds)

	bar := progressbar.Default(int64(n_seeds))

	for i := range inp.seeds {
		if i%2 == 0 {
			seed_start := inp.seeds[i]
			n_rep := inp.seeds[i+1]
			for seed := seed_start; seed < seed_start+n_rep; seed++ {
				v := queryAll(inp.groups, seed)
				res = min(res, v)
			}
			bar.Add(n_rep)
		}
	}

	return res
}

func main() {
	input, err := loadInput()
	if err != nil {
		fmt.Println(err)
	}

	//fmt.Println(inputs)

	//fmt.Println(input.groups[0])
	//fmt.Println(query(input.groups[0], 79))
	//fmt.Println(query(input.groups[0], 14))
	//fmt.Println(query(input.groups[0], 55))
	//fmt.Println(query(input.groups[0], 13))

	fmt.Println("Part1 =", input.Part1())

	// 28797563 it/s
	fmt.Println("Part2 =", input.Part2())
}
