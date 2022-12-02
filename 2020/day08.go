package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type Instruction struct {
	code string
	val  int
}

func loadInput(path string) []Instruction {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		fmt.Println("Failed to read input file", err)
		return []Instruction{}
	}

	strs := strings.Split(strings.TrimSuffix(string(data), "\n"), "\n")
	ins_arr := make([]Instruction, len(strs))
	for i, str := range strs {
		instruction := strings.Split(str, " ")
		code := instruction[0]
		val, err := strconv.Atoi(instruction[1])
		if err != nil {
			fmt.Println("Failed to parse instruction: ", instruction)
			return []Instruction{}
		}
		ins_arr[i] = Instruction{code, val}
	}
	return ins_arr
}

func solPart1(data []Instruction) int {
	data_len := len(data)
	visited := make([]uint8, data_len)
	i := 0   // instruction pointer
	acc := 0 // global accumulator
	for {
		if i >= data_len || visited[i] == 1 {
			break
		}
		visited[i] = 1
		ins := data[i]

		switch ins.code {
		case "acc":
			acc += ins.val
			i += 1
		case "jmp":
			i += ins.val
		case "nop":
			i += 1
		}
	}
	return acc
}

func runProg(data []Instruction) (int, error) {
	data_len := len(data)
	visited_mp := make([]uint8, data_len)
	i := 0   // instruction pointer
	acc := 0 // global accumulator

	for {
		if i >= data_len {
			break
		}
		if visited_mp[i] == 1 {
			return -1, errors.New("Visitng an instruction twice")
		}
		visited_mp[i] = 1

		ins := data[i]

		switch ins.code {
		case "acc":
			acc += ins.val
			i += 1
		case "jmp":
			if i == data_len-2 {
				i += 1 // convert to NOP
			} else {
				i += ins.val // stay as JMP
			}
		case "nop":
			tmp := i + ins.val
			if tmp == data_len-2 || tmp == data_len {
				i += ins.val // convert to JMP
			} else {
				i += 1 // stay as NOP
			}
		}
	}
	return acc, nil
}

func solPart2(data []Instruction) (int, error) {
	for i, ins := range data {
		if ins.code == "jmp" {
			data[i].code = "nop"
			res, err := runProg(data)
			if err != nil {
				data[i].code = "jmp"
			} else {
				return res, nil
			}
		} else if ins.code == "nop" {
			data[i].code = "jmp"
			res, err := runProg(data)
			if err != nil {
				data[i].code = "nop"
			} else {
				return res, nil
			}
		}
	}
	return -1, errors.New("solution not found")
}

func main() {
	data := loadInput("./day08input.txt")
	// res := solPart1(data)
	// fmt.Println("Part 1: ", res)
	res, err := solPart2(data)
	if err != nil {
		fmt.Println("Failed ")
	}
	fmt.Println("Part 2: ", res)
}
