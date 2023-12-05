package graph

import (
	"container/heap"
	"reflect"
	"testing"
)

func TestPriorityQueue(t *testing.T) {
	pq := &Heap{}
	heap.Init(pq)
	heap.Push(pq, HeapItem{distance: 1, node: "A"})
	heap.Push(pq, HeapItem{distance: 2, node: "B"})
	heap.Push(pq, HeapItem{distance: 3, node: "C"})
	heap.Push(pq, HeapItem{distance: 4, node: "D"})

	expected_order := []string{"A", "B", "C", "D"}
	for _, expect := range expected_order {
		if node := heap.Pop(pq).(HeapItem).node; node != expect {
			t.Errorf(`Wrong order. Expected %v, got %v`, expect, node)
		}
	}

	// Test random insersion
	heap.Push(pq, HeapItem{distance: 2, node: "B"})
	heap.Push(pq, HeapItem{distance: 1, node: "A"})
	heap.Push(pq, HeapItem{distance: 4, node: "D"})
	heap.Push(pq, HeapItem{distance: 3, node: "C"})
	for _, expect := range expected_order {
		if node := heap.Pop(pq).(HeapItem).node; node != expect {
			t.Errorf(`Wrong order. Expected %v, got %v`, expect, node)
		}
	}

	// Test stability
	heap.Push(pq, HeapItem{distance: 2, node: "A"})
	heap.Push(pq, HeapItem{distance: 2, node: "B"})
	expected_order = []string{"A", "B"}
	for _, expect := range expected_order {
		if node := heap.Pop(pq).(HeapItem).node; node != expect {
			t.Errorf(`Wrong order. Expected %v, got %v`, expect, node)
		}
	}
}

func TestDijkstra(t *testing.T) {

	// Constant distance
	get_distance := func(a, b string) int {
		return 1
	}

	sd, err := Dijkstra("A", map[string][]string{"A": {"B"}, "B": {"A"}}, get_distance)
	if err != nil {
		t.Errorf(`Error occured in Dijkstra: %v`, err)
	}
	if !reflect.DeepEqual(sd, map[string]int{"A": 0, "B": 1}) {
		t.Error(`Wrong result`)
	}

	sd, err = Dijkstra("A",
		map[string][]string{
			"A": {"B"},
			"B": {"A", "C", "D"},
			"C": {"B", "D"},
			"D": {"B", "C"},
		},
		get_distance,
	)
	if err != nil {
		t.Errorf(`Error occured in Dijkstra: %v`, err)
	}
	if !reflect.DeepEqual(sd, map[string]int{
		"A": 0,
		"B": 1,
		"C": 2,
		"D": 2,
	}) {
		t.Error(`Wrong result`)
	}

}
