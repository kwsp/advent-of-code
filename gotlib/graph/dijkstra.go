package graph

import (
	"container/heap"
)

type HeapItem struct {
	distance int // distance
	node     string
}
type Heap []HeapItem

func (h Heap) Len() int            { return len(h) }
func (h Heap) Less(i, j int) bool  { return h[i].distance < h[j].distance }
func (h Heap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *Heap) Push(x interface{}) { *h = append(*h, x.(HeapItem)) }
func (h *Heap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

// Dijkstra's Algorithm
// Return the shortest distance from the start node to every other node.
// get_distance is a function that returns the distance between a pair of edges
func Dijkstra(start string, edges map[string][]string, get_distance func(string, string) int) (map[string]int, error) {
	visited := map[string]bool{}
	sd := make(map[string]int)
	var err error

	// priority queue sorted by distance
	tovisit := &Heap{}
	heap.Push(tovisit, HeapItem{distance: 0, node: start})
	sd[start] = 0
	for len(*tovisit) > 0 {
		curr := heap.Pop(tovisit).(HeapItem)
		visited[curr.node] = true
		for _, neighbor := range edges[curr.node] {
			if _, ok := visited[neighbor]; ok {
				continue
			}

			newdistance := sd[curr.node] + get_distance(curr.node, neighbor)
			if _, ok := sd[neighbor]; ok {
				sd[neighbor] = min(sd[neighbor], newdistance)
			} else {
				sd[neighbor] = newdistance
			}
			heap.Push(tovisit, HeapItem{distance: sd[neighbor], node: neighbor})

		}
	}

	return sd, err
}
