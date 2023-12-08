package graph

import (
	"container/heap"
)

type HeapItem[K comparable] struct {
	distance int // distance
	node     K
}
type Heap[K comparable] []HeapItem[K]

func (h Heap[K]) Len() int            { return len(h) }
func (h Heap[K]) Less(i, j int) bool  { return h[i].distance < h[j].distance }
func (h Heap[K]) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *Heap[K]) Push(x interface{}) { *h = append(*h, x.(HeapItem[K])) }
func (h *Heap[K]) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

// Dijkstra's Algorithm
// Return the shortest distance from the start node to every other node.
// get_distance is a function that returns the distance between a pair of edges
func Dijkstra[K comparable](start K, edges map[K][]K, get_distance func(K, K) int) (map[K]int, error) {
	visited := map[K]bool{}
	sd := make(map[K]int) // shortest distances
	var err error

	// priority queue sorted by distance
	tovisit := &Heap[K]{}
	heap.Push(tovisit, HeapItem[K]{distance: 0, node: start})
	sd[start] = 0
	for len(*tovisit) > 0 {
		curr := heap.Pop(tovisit).(HeapItem[K])
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
			heap.Push(tovisit, HeapItem[K]{distance: sd[neighbor], node: neighbor})

		}
	}

	return sd, err
}
