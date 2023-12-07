package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Input struct {
	hands string
	bid   int
	ctype int
}

var CARDS string = "AKQJT98765432"
var NCARDS int = len(CARDS)

func getCardValue(c byte) (int, error) {
	for i := 0; i < NCARDS; i++ {
		if c == CARDS[i] {
			return NCARDS - i, nil
		}
	}
	return -1, errors.New("Card not found")
}

type Inputs []Input

func (inputs Inputs) Len() int      { return len(inputs) }
func (inputs Inputs) Swap(i, j int) { inputs[i], inputs[j] = inputs[j], inputs[i] }
func (inputs Inputs) Less(i, j int) bool {
	if inputs[i].ctype == inputs[j].ctype {
		// Tie breaker by card
		for k := 0; k < 5; k++ {
			ci, err := getCardValue(inputs[i].hands[k])
			if err != nil {
				log.Fatal(err)
			}
			cj, err := getCardValue(inputs[j].hands[k])
			//fmt.Printf("Compare %c (%v) %c (%v)\n", inputs[i].hands[k], ci, inputs[j].hands[k], cj)
			if err != nil {
				log.Fatal(err)
			}
			if ci == cj {
				continue
			} else {
				return ci < cj
			}
		}
	}
	return inputs[i].ctype < inputs[j].ctype
}

// Five of a kind, where all five cards have the same label: AAAAA
// Four of a kind, where four cards have the same label and one card has a different label: AA8AA
// Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
// Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
// Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
// One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
// High card, where all cards' labels are distinct: 23456
func (inp *Input) updateCountAndRank() {
	cardCount := map[rune]int{}
	for _, c := range inp.hands {
		val, ok := cardCount[c]
		if !ok {
			cardCount[c] = 1
		} else {
			cardCount[c] = val + 1
		}
	}
	counts := [6]int{}
	for _, n := range cardCount {
		counts[n] += 1
	}

	if counts[5] == 1 {
		// Five of a kind
		//fmt.Println("Five of a kind")
		inp.ctype = 6
	} else if counts[4] == 1 {
		//fmt.Println("Four of a kind")
		inp.ctype = 5
	} else if counts[3] == 1 {
		if counts[2] == 1 {
			//fmt.Println("Full house")
			inp.ctype = 4
		} else {
			//fmt.Println("Three of a kind")
			inp.ctype = 3
		}
	} else if counts[2] == 2 {
		//fmt.Println("Two pair")
		inp.ctype = 2
	} else if counts[2] == 1 {
		//fmt.Println("One pair")
		inp.ctype = 1
	} else if counts[1] == 5 {
		//fmt.Println("High card")
		inp.ctype = 0
	} else {
		log.Fatal("Unknown input", inp)
	}
}

func (inp *Input) updateCountAndRankJoker() {
	cardCount := map[rune]int{}
	for _, c := range inp.hands {
		val, ok := cardCount[c]
		if !ok {
			cardCount[c] = 1
		} else {
			cardCount[c] = val + 1
		}
	}
	counts := [6]int{}
	nJokers := 0
	for c, n := range cardCount {
		if c == 'J' {
			nJokers += n
		} else {
			counts[n] += 1
		}
	}

	if nJokers > 0 {
		for i := 4; i >= 0; i-- {
			if counts[i] > 0 {
				counts[i+nJokers] += 1
				counts[i] -= 1
				break
			}
		}
	}

	if counts[5] == 1 || nJokers == 5 {
		// Five of a kind
		//fmt.Println("Five of a kind")
		inp.ctype = 6
	} else if counts[4] == 1 {
		//fmt.Println("Four of a kind")
		inp.ctype = 5
	} else if counts[3] == 1 {
		if counts[2] == 1 {
			//fmt.Println("Full house")
			inp.ctype = 4
		} else {
			//fmt.Println("Three of a kind")
			inp.ctype = 3
		}
	} else if counts[2] == 2 {
		//fmt.Println("Two pair")
		inp.ctype = 2
	} else if counts[2] == 1 {
		//fmt.Println("One pair")
		inp.ctype = 1
	} else if counts[1] == 5 {
		//fmt.Println("High card")
		inp.ctype = 0
	} else {
		log.Fatal("Unknown input", inp)
	}
}

func parseLine(line string) (Input, error) {
	fields := strings.Fields(line)
	bid, err := strconv.Atoi(fields[1])
	inp := Input{hands: fields[0], bid: bid}
	inp.updateCountAndRank()
	return inp, err
}

func loadInput() (Inputs, error) {
	f, err := os.Open("inp.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	var inputs []Input
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

func main() {
	inputs, err := loadInput()
	if err != nil {
		fmt.Println(err)
	}

	sort.Sort(inputs)

	part1 := 0
	for i, inp := range inputs {
		part1 += (i + 1) * inp.bid
	}

	fmt.Println("Part1 =", part1)

	for i := range inputs {
		inputs[i].updateCountAndRankJoker()
	}

	CARDS = "AKQT98765432J"
	sort.Sort(inputs)

	part2 := 0
	for i, inp := range inputs {
		part2 += (i + 1) * inp.bid
	}
	fmt.Println("Part2 =", part2)
}
