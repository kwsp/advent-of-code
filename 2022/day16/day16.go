package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/kwsp/gotlib/graph"
	"github.com/schollz/progressbar/v3"
)

type Input struct {
	name    string
	val     int
	leadsto []string
}

func parseLine(line string) (Input, error) {
	lineparts := strings.SplitN(line, ";", 2)

	left := lineparts[0]
	leftsplit := strings.Split(left, " ")
	name := leftsplit[1]
	frate, err := strconv.Atoi(strings.Split(leftsplit[len(leftsplit)-1], "=")[1])
	if err != nil {
		return Input{}, err
	}

	right := lineparts[1]
	leadsto_s := strings.SplitN(right, " ", 6)[5]

	inp := Input{name: name, val: frate, leadsto: strings.Split(leadsto_s, ", ")}
	return inp, err
}

func loadInput() ([]Input, error) {
	f, err := os.Open("day16.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	var inputs []Input
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		// Handle line parsing here
		line := scanner.Text()
		inp, err := parseLine(line)
		if err != nil {
			log.Fatal(err)
			break
		}
		inputs = append(inputs, inp)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return inputs, err
}

type Worker struct {
	time int    // Time remaining for this worker
	node string // Node worker is currently at
}
type State1 struct {
	released  int
	workers   []Worker
	unvisited []string
}
type Heap1 []State1                 // Max heap over `released`
func (s Heap1) Len() int            { return len(s) }
func (s Heap1) Less(i, j int) bool  { return s[i].released > s[j].released }
func (s Heap1) Swap(i, j int)       { s[i], s[j] = s[j], s[i] }
func (s *Heap1) Push(x interface{}) { *s = append(*s, x.(State1)) }
func (s *Heap1) Pop() interface{} {
	old := *s
	n := len(old)
	x := old[n-1]
	*s = old[0 : n-1]
	return x
}

func main() {
	inputs, err := loadInput()
	if err != nil {
		log.Fatal(err)
	}

	// Parse into a graph
	nodes := make(map[string]int)
	edges := make(map[string][]string)
	for _, inp := range inputs {
		nodes[inp.name] = inp.val
		edges[inp.name] = inp.leadsto
	}

	worthy_nodes := []string{}
	for node, v := range nodes {
		if v > 0 {
			worthy_nodes = append(worthy_nodes, node)
		}
	}

	get_distance := func(a, b string) int { return 1 }
	shortest_distances := map[[2]string]int{}
	for _, node := range append(worthy_nodes, "AA") {
		sd, err := graph.Dijkstra(node, edges, get_distance)
		if err != nil {
			break
		}
		for neighbor, d := range sd {
			shortest_distances[[2]string{node, neighbor}] = d
			shortest_distances[[2]string{neighbor, node}] = d
		}
	}

	solution := func(q1 *Heap1) int {
    bar := progressbar.Default(-1)
		//bar := progressbar.NewOptions(-1,)

		best_released := 0
		for q1.Len() > 0 {
			state := heap.Pop(q1).(State1)
			bar.Add(len(state.unvisited))

			for _, tovisit := range state.unvisited {
				for worker_i, worker := range state.workers {
					distance := shortest_distances[[2]string{worker.node, tovisit}]
					newtime := worker.time - distance - 1

					if newtime <= 0 {
						continue
					}

					newreleased := state.released + nodes[tovisit]*newtime

					if newreleased > best_released {
						best_released = newreleased
						// bar. update description
						bar.Describe(fmt.Sprintf("[Best so far = %v]", best_released))
					}

					if len(state.unvisited) > 1 {
						new_unvisited := make([]string, 0, len(state.unvisited)-1)
						for _, node := range state.unvisited {
							if node != tovisit {
								new_unvisited = append(new_unvisited, node)
							}
						}

						newworkers := []Worker{{node: tovisit, time: newtime}}
						for i, w := range state.workers {
							if i != worker_i {
								newworkers = append(newworkers, w)
							}
						}

						heap.Push(q1,
							State1{
								workers:   newworkers,
								unvisited: new_unvisited,
								released:  newreleased,
							},
						)
					}
				}
			}
		}

		bar.Close()
		return best_released
	}

	part1 := solution(&Heap1{
		State1{
			released:  0,
			workers:   []Worker{{time: 30, node: "AA"}},
			unvisited: worthy_nodes,
		},
	})
	fmt.Println("Part1 =", part1)

	part2 := solution(&Heap1{
		State1{
			released:  0,
			workers:   []Worker{{time: 26, node: "AA"}, {time: 26, node: "AA"}},
			unvisited: worthy_nodes,
		},
	})
	fmt.Println("Part2 =", part2)
}
