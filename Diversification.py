import random


class Diversification:
    def __init__(self):
        pass

    def diversification(self, graph):

        ALFA = random.random()
        S = []  # labeld vertex
        U = graph.nodes()  # unlabed vertex
        f = {}  # vertex order
        CW = {}
        k = 1

        min_vertex = min(graph.degree(), key=graph.degree().get)
        f[k] = min_vertex
        CW[min_vertex] = len(graph.neighbors(min_vertex))
        S.append(min_vertex)
        U.remove(min_vertex)

        while len(U) > 0:
            k += 1
            CL = []  # candidate list
            for v in S:
                for n_v in graph.neighbors(v):
                    if not S.__contains__(n_v):
                        CL.append(n_v)

            # CW_all = self.cutwidth_for_all_vertex(graph, CW, f)
            CW_v = {}
            for v in CL:
                CW_v[v] = self.count_CW_for_vertex(graph, CW, v, f[k - 1])

            min_vertex = min(CW_v, key=CW_v.get)
            max_vertex = max(CW_v, key=CW_v.get)
            CW_min = CW_v[min_vertex]
            CW_max = CW_v[max_vertex]

            RCL = {}  # restricted candidate list
            for v in CL:
                if CW_v[v] <= CW_min + ALFA * (CW_max - CW_min):
                    RCL[v] = CW_v[v]
            vertex = random.choice(RCL.keys())
            self.set_vertex_to_CW(graph, CW, f, vertex, k)
            f[k] = vertex
            S.append(vertex)
            U.remove(vertex)
        return f, CW, self.get_cutwidth_of_graph(CW)

    def set_vertex_to_CW(self, graph, CW, f, v, k):

        n_labeled = 0
        n_unlabeled = 0
        neighbors = graph.neighbors(v)
        for n_v in neighbors:
            if f.values().__contains__(n_v):
                n_labeled += 1
            else:
                n_unlabeled += 1

        CW[v] = int(CW[f[k - 1]]) - n_labeled + n_unlabeled
        return CW

    def count_CW_for_vertex(self, graph, CW, v, prev_v):
        if len(CW) <= 0:
            return 0

        n_labeled = 0
        n_unlabeled = 0
        neighbors = graph.neighbors(v)
        for n_v in neighbors:
            if CW.__contains__(n_v):
                n_labeled += 1
            else:
                n_unlabeled += 1
        return int(CW[prev_v]) - n_labeled + n_unlabeled

    def get_cutwidth_of_graph(self, CW):
        return CW[max(CW, key=CW.get)]
