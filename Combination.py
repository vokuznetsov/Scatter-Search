import networkx as nx
import Diversification
import Improvement


class Combination:
    def __init__(self, graph):
        self.dv = Diversification.Diversification()
        self.im = Improvement.Improvement(graph)
        self.graph = graph
        pass

    def get_min_cw(self, graph, CW, f_12_last_vertex, f1_vertex, f2_vertex):
        # n_left_1, n_right_1 = self.im.get_left_right_neigbors(graph, f_12, int(f1[i]), i)
        # cw_1 = CW[f_12[i - 1]] + n_right_1 - n_left_1
        # n_left_2, n_right_2 = self.im.get_left_right_neigbors(graph, f_12, int(f2[i]), i)
        # cw_2 = CW[f_12[i - 1]] + n_right_2 - n_left_2

        cw_1 = self.dv.count_CW_for_vertex(graph, CW, f1_vertex, f_12_last_vertex)
        cw_2 = self.dv.count_CW_for_vertex(graph, CW, f2_vertex, f_12_last_vertex)

        if cw_1 < cw_2:
            return '1', cw_1
        else:
            return '2', cw_2

    def remove_vertex(self, f1, f2, vertex):
        f1_label = self.im.get_label_by_vertex(f1, vertex)
        f1.pop(f1_label)
        f2_label = self.im.get_label_by_vertex(f2, vertex)
        f2.pop(f2_label)

        return f1, f2

    def remove_vertex_from_CW(self, CW_1, CW_2, vertex):
        CW_1.pop(vertex)
        CW_2.pop(vertex)
        return CW_1, CW_2

    def get_label_vertex(self, tuple):
        return tuple[0], tuple[1]

    def combination_2(self, f_1, f_2):
        f = {}
        CW_1 = self.im.compute_cutwidth_by_labeling(self.graph, f_1)
        CW_2 = self.im.compute_cutwidth_by_labeling(self.graph, f_2)

        for i in range(1, len(CW_1) + 1):
            cw_1_sort = sorted(CW_1.items(), key=lambda x: x[1])
            cw_2_sort = sorted(CW_2.items(), key=lambda x: x[1])
            v1, cw1 = cw_1_sort[0]
            v2, cw2 = cw_2_sort[0]
            if cw1 < cw2:
                f[i] = v1
                self.remove_vertex_from_CW(CW_1, CW_2, v1)
            else:
                f[i] = v2
                self.remove_vertex_from_CW(CW_1, CW_2, v2)
        CW = self.im.compute_cutwidth_by_labeling(self.graph, f)
        CW_G = self.dv.get_cutwidth_of_graph(CW)
        return f, CW, CW_G

    def combination_3(self, f_1, f_2):
        f1 = f_1.copy()
        f2 = f_2.copy()
        f_12 = {}
        CW = {}
        for i in range(1, len(f_1) + 1):
            l1, v1 = f1.iteritems().next()
            l2, v2 = f2.iteritems().next()
            if i == 1:
                neigh_1 = len(self.graph.neighbors(v1))
                neigh_2 = len(self.graph.neighbors(v2))
                if neigh_1 < neigh_2:
                    f_12[i] = v1
                    CW[v1] = neigh_1
                    f1, f2 = self.remove_vertex(f1, f2, v1)
                else:
                    f_12[i] = v2
                    CW[v2] = neigh_2
                    f1, f2 = self.remove_vertex(f1, f2, v2)
            else:
                n, value = self.get_min_cw(self.graph, CW, f_12[i - 1], v1, v2)
                if n == '1':
                    f_12[i] = v1
                    CW[v1] = value
                    f1, f2 = self.remove_vertex(f1, f2, v1)
                else:
                    f_12[i] = v2
                    CW[v2] = value
                    f1, f2 = self.remove_vertex(f1, f2, v2)

        # print 'CW_combination: ' + str(self.dv.get_cutwidth_of_graph(CW))
        return f_12, CW, self.dv.get_cutwidth_of_graph(CW)
