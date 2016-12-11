import networkx as nx


def parser(graph_name):
    path = "graphs/" + str(graph_name)

    graph = nx.Graph()
    f = open(path, 'r')
    [n_verticies, n_edges] = f.readline().strip().split(' ')

    for line in f:
        [v1, v2] = line.strip().split(' ')
        graph.add_edge(v1, v2)

    if n_verticies == graph.node:
        print 'true'
    if n_edges == graph.edge:
        print 'true'
    return graph