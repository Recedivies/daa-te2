from generator import Generator
import networkx as nx
import datetime
import os, psutil
import operator


def vc_size(current_vc):
    # VC is a tuple list, where each tuple = (node_ID, state) vc_size is the number of nodes has state == 1
    vc_size = 0
    for element in current_vc:
        vc_size += element[1]
    return vc_size


# returns the max degree node in a given any graph
def max_deg(g):
    deglist = list(g.degree())
    deglist_sorted = sorted(
        deglist, reverse=True, key=operator.itemgetter(1)
    )  # sort in descending order of node degree
    v = deglist_sorted[0]  # tuple - (node,degree)
    return v


def branch_and_bound(G):
    process = psutil.Process()
    start_time = datetime.datetime.now()

    current_graph = (
        G.copy()
    )  # current_graph: sub-graph of current graph after removing the explored nodes
    best_vertex_cover = (
        []
    )  # best_vertex_cover: min (best) Vertex cover for a given sub-graph
    current_vc = []  # current_vc: Vertex cover for a given sub-graph
    frontier = []
    vertex = max_deg(current_graph)
    frontier.append((vertex[0], 0, (-1, -1)))
    frontier.append((vertex[0], 1, (-1, -1)))
    upper_bound = G.number_of_nodes()

    while len(frontier) != 0:
        (
            vertex_i,
            state,
            parent_node,
        ) = frontier.pop()  # the current node, last node of the frontier set

        backtrack = False
        if state == 1:
            current_graph.remove_node(vertex_i)  # remove the vertex from current_graph

        elif state == 0:
            neighbor = current_graph.neighbors(vertex_i)
            for node in list(neighbor):
                current_graph.remove_node(node)
                current_vc.append((node, 1))  # add all the neigbor to the Vertex Cover

        current_vc.append((vertex_i, state))
        current_vc_size = vc_size(current_vc)

        if current_graph.number_of_edges() == 0:  # done exploring
            if current_vc_size < upper_bound:
                best_vertex_cover = current_vc.copy()
                upper_bound = current_vc_size
            backtrack = True

        else:
            max_degree_vertex = max_deg(current_graph)
            lb = (
                current_graph.number_of_edges() // max_degree_vertex[1]
            )  # lower bound calcuation
            current_lower_bound = lb + current_vc_size  # reset lower bound
            if upper_bound > current_lower_bound:  # worth exploring
                frontier.append((max_degree_vertex[0], 0, (vertex_i, state)))
                frontier.append((max_degree_vertex[0], 1, (vertex_i, state)))
            else:
                backtrack = True

        if backtrack and len(frontier) != 0:  # backtrack to explore other nodes.
            last_frontier = frontier[-1][2]  # parent node
            if last_frontier in current_vc:
                while current_vc.index(last_frontier) + 1 < len(
                    current_vc
                ):  # undoing changes from the end of current Vertex cover to parent node
                    (
                        node_i,
                        state_i,
                    ) = current_vc.pop()  # remove what we added to Current Vertex Cover
                    list_of_nodes = list(map(lambda t: t[0], current_vc))
                    current_graph.add_node(
                        node_i
                    )  # add back what we deleted from the Current Graph
                    for node in G.neighbors(node_i):
                        if (node in current_graph.nodes()) and (
                            node not in list_of_nodes
                        ):
                            current_graph.add_edge(node, node_i)
            else:
                # backtrack to the root node
                current_graph = G.copy()
                current_vc.clear()

    end_time = datetime.datetime.now()
    time_diff = end_time - start_time
    execution_time = time_diff.total_seconds() * 1000
    print(
        f"[BnB]: "
        f"Execution time: {execution_time:.1f} ms, "
        f"Memory Usage: {process.memory_info().rss // 1_000_000} MB"  # in MB
    )

    return best_vertex_cover


def bnb_main(G_bnb):
    final_VC = branch_and_bound(G_bnb)

    min_vc = []  # make a list of vertex cover nodes
    for i in final_VC:
        if i[1] == 1:
            min_vc.append(i)

    # minimum size vertex cover
    return len(min_vc)
