from collections import defaultdict
from heapq import heappush, heappop


with open("./day16_.txt", "r") as fp:
    lines = [line.rstrip("\n") for line in fp]


def pline(s: str):
    "Parse line"
    a, b = s.split(";", 1)
    aa = a.split(" ")
    vname = aa[1]
    flow = int(aa[-1].split("=")[1])
    leadsto = b.split(" ", 5)[-1]
    return vname, flow, tuple(leadsto.split(", "))


NODES: dict[str, int] = {}
EDGES: dict[str, tuple[str, ...]] = {}
inp = [pline(l) for l in lines]
for name, flow, edges in inp:
    NODES[name] = flow
    EDGES[name] = edges

# # visualize
# import graphviz
# dot = graphviz.Graph(strict=True)  # strict removes duplicate edges
# for name, flow, leadsto in inp:
# dot.node(name, f"{name} ({flow})")
# for _name in leadsto:
# dot.edge(name, _name)
# dot.render("day16")

"""
Start at AA. Can move anywhere. Try to maximize flow rate
Nodes worth visiting are nodes with nonzero flowrate.
First use Dijkstra's Algorithm to compute the shortest distance between
all the nodes worth visiting and AA
"""


def dijkstra(start: str, edges: dict[str, tuple[str, ...]]) -> dict[str, int]:
    "Returns the shortest distance from `start` to all nodes"
    visited = set()
    # shortest distance
    sd: dict[str, int] = defaultdict(lambda: 2 << 31)
    tovisit = []
    heappush(tovisit, (0, start))
    sd[start] = 0
    while tovisit:
        _, node = heappop(tovisit)
        visited.add(node)
        for neighbor in edges[node]:
            if neighbor in visited:
                continue
            # All edge weights are 1 here
            sd[neighbor] = min(sd[neighbor], sd[node] + 1)
            heappush(tovisit, (sd[neighbor], neighbor))
    return sd


worthy_nodes = [k for k, v in NODES.items() if v]
shortest_distances: dict[tuple[str, str], int] = {}
for node in (*worthy_nodes, "AA"):
    sd = dijkstra(node, EDGES)
    for neighbor, d in sd.items():
        if neighbor in worthy_nodes:
            shortest_distances[(neighbor, node)] = d
            shortest_distances[(node, neighbor)] = d


from typing import NamedTuple


class State1(NamedTuple):
    priority: int
    node: str
    time: int
    unvisited: list[str]
    released: int = 0


part1 = 0
queue: list[State1] = [
    State1(
        priority=0,
        node="AA",
        time=30,
        unvisited=worthy_nodes,
    )
]

while queue:
    state = heappop(queue)
    node = state.node
    print(state)

    # move to a worthy node and open
    for tovisit in state.unvisited:
        distance = shortest_distances[(state.node, tovisit)]
        newtime = state.time - distance - 1
        if newtime > 0:
            newreleased = state.released + NODES[tovisit] * newtime
            part1 = max(part1, newreleased)
            new_unvisited = [n for n in state.unvisited if n != tovisit]
            if len(state.unvisited) > 1:
                newstate = State1(
                    node=tovisit,
                    time=newtime,
                    unvisited=new_unvisited,
                    released=newreleased,
                    priority=-newreleased,
                )
                heappush(queue, newstate)

print(f"{part1=}")


class Worker(NamedTuple):
    time: int
    node: str


class State2(NamedTuple):
    priority: int
    workers: list[Worker]
    unvisited: list[str]
    released: int = 0
    # checked_edge: dict[tuple[str, str], int]


part2 = 0
# queue_p2: PriorityQueue[State2] = PriorityQueue()
# queue_p2.put(
# State2(
# priority=0,
# workers=(Worker(node="AA", time=26), Worker(node="AA", time=26)),
# worthy_unvisited=list(worthy_nodes),
# )
# )
queue_p2: list[State2] = [
    State2(
        priority=0,
        workers=[Worker(node="AA", time=26), Worker(node="AA", time=26)],
        unvisited=list(worthy_nodes),
    )
]


import tqdm


class AStarRecord(NamedTuple):
    time: int
    released: int


astar: dict[str, list[AStarRecord]] = {}
import bisect


bar = tqdm.tqdm(desc="[Part 2]", disable=False)
while queue_p2:
    state = heappop(queue_p2)
    # workers sorted by time. use last worker (largest time remaining)

    # move to a worthy node and open
    bar.update(len(state.unvisited))
    for tovisit in state.unvisited:

        # do combinations of both workers
        for worker_i, worker in enumerate(state.workers):
            distance = shortest_distances[(worker.node, tovisit)]
            newtime = worker.time - distance - 1

            # print(newtime, state.worthy_unvisited)
            if newtime > 0:
                newreleased = state.released + NODES[tovisit] * newtime

                """
                If a node was checked at an earlier time
                with a higher released score, ignore this check?
                This may not be a valid heuristic
                """
                # discard_edge = False
                # if astar_records := astar.get(worthy_node, None):
                # idx = bisect.bisect_left(astar_records, newtime, key=lambda r: r.time)
                # oldrec= astar_records[idx]
                # if oldrec.released >= newreleased:
                # discard_edge=True
                # else:
                # # If record for this time exists, update it
                # # otherwise, insert it
                # newrec = AStarRecord(time=newtime, released=newreleased)
                # if oldrec.time == newtime:
                # astar_records[idx] = newrec
                # else:
                # astar_records.insert(idx, newrec)
                # else:
                # astar[worthy_node] = [AStarRecord(time=newtime, released=newreleased)]

                # if not discard_edge:

                if newreleased > part2:
                    part2 = newreleased
                    bar.set_description_str(f"Part 2 [best={part2}]")

                if len(state.unvisited) > 1:
                    newworkers = [
                        Worker(node=tovisit, time=newtime),
                        *(w for i, w in enumerate(state.workers) if i != worker_i),
                    ]
                    # print(f"Moving {worker.node} -> {worthy_node}, time={newtime} released={newreleased}, workers={newworkers}")

                    new_unvisited = state.unvisited.copy()
                    new_unvisited.remove(tovisit)

                    newstate = State2(
                        workers=newworkers,
                        unvisited=new_unvisited,
                        released=newreleased,
                        priority=-newreleased,
                    )
                    heappush(queue_p2, newstate)

bar.close()

# Tried 2720. Too low
# Tried 2786 not correct
# New 2824
print(f"{part2=}")

# perf with PriorityQueue   1284152.86it/s
# Perf with heapq           2243522.43it/s
breakpoint()
