package graph

import (
	"container/heap"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPriorityQueue(t *testing.T) {
	pq := &Heap[string]{}
	heap.Init(pq)
	heap.Push(pq, HeapItem[string]{distance: 1, node: "A"})
	heap.Push(pq, HeapItem[string]{distance: 2, node: "B"})
	heap.Push(pq, HeapItem[string]{distance: 3, node: "C"})
	heap.Push(pq, HeapItem[string]{distance: 4, node: "D"})

	expected_order := []string{"A", "B", "C", "D"}
	for _, expect := range expected_order {
		assert.Equal(t, expect, heap.Pop(pq).(HeapItem[string]).node)
	}

	// Test random insersion
	heap.Push(pq, HeapItem[string]{distance: 2, node: "B"})
	heap.Push(pq, HeapItem[string]{distance: 1, node: "A"})
	heap.Push(pq, HeapItem[string]{distance: 4, node: "D"})
	heap.Push(pq, HeapItem[string]{distance: 3, node: "C"})
	for _, expect := range expected_order {
		assert.Equal(t, expect, heap.Pop(pq).(HeapItem[string]).node)
	}

	// Test stability
	heap.Push(pq, HeapItem[string]{distance: 2, node: "A"})
	heap.Push(pq, HeapItem[string]{distance: 2, node: "B"})
	expected_order = []string{"A", "B"}
	for _, expect := range expected_order {
		assert.Equal(t, expect, heap.Pop(pq).(HeapItem[string]).node)
	}
}

func TestDijkstra(t *testing.T) {

	// Constant distance
	get_distance := func(a, b string) int {
		return 1
	}

	sd, err := Dijkstra("A", map[string][]string{"A": {"B"}, "B": {"A"}}, get_distance)
	assert.Equal(t, nil, err)
	assert.Equal(t, map[string]int{"A": 0, "B": 1}, sd)

	sd, err = Dijkstra("A",
		map[string][]string{
			"A": {"B"},
			"B": {"A", "C", "D"},
			"C": {"B", "D"},
			"D": {"B", "C"},
		},
		get_distance,
	)
	assert.Equal(t, nil, err)
	assert.Equal(t, map[string]int{"A": 0, "B": 1, "C": 2, "D": 2}, sd)

}
