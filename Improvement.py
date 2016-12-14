import numpy as np
import networkx as nx
import random
import Parser
import Diversification


class Improvement:
    def __init__(self, graph):
        self.dv = Diversification.Diversification()
        self.graph = graph
        # self.f = f
        # self.CW = CW
        # self.CW_G = CW_G
        pass

    def get_label_by_vertex(self, f, vertex):
        for label, v in f.iteritems():
            if v == vertex:
                return label

    def update_dict(self, dict, key_from, key_to, reverse=False):
        if reverse:
            for i in range(key_to, key_from - 1, -1):
                temp = {i: dict[i]}
                dict.pop(i)
                dict[i + 1] = temp[i]
                temp.clear()
        else:
            for i in range(key_from, key_to + 1):
                temp = {i: dict[i]}
                dict.pop(i)
                dict[i - 1] = temp[i]
                temp.clear()
        return dict

    def get_left_right_neigbors(self, graph, f, vertex, pos):
        neighbors = graph.neighbors(vertex)
        n_left = 0
        n_right = 0
        for v in neighbors:
            pos_v = self.get_label_by_vertex(f, v)
            if pos_v <= pos:
                n_left += 1
            else:
                n_right += 1
        return n_left, n_right

    # recompute cutwidth for moving vertex
    def recompute_cutwidth_for_one_vertex(self, CW_new, f_new, vertex, new_position, old_position_higher=False):
        pos_before_vertex = new_position - 1
        cw_prev_v = CW_new[f_new[pos_before_vertex]]
        n_left, n_right = self.get_left_right_neigbors(self.graph, f_new, vertex, new_position)
        CW_new.pop(vertex)
        if old_position_higher:
            CW_new[vertex] = cw_prev_v + n_right
        else:
            CW_new[vertex] = cw_prev_v - n_left + n_right
        return CW_new

    # recompute cutwidth for vertices between new and old_position of moving vertex
    def recompute_cutwidth_for_inserted_vertices(self, CW_new, f_old, f_new, vertex, pos, old_position_higher=False):
        v = f_new[pos]
        cw_old = CW_new[v]
        prev_pos = self.get_label_by_vertex(f_old, v)
        n_left, n_right = self.get_left_right_neigbors(self.graph, f_old, vertex, prev_pos)
        CW_new.pop(v)
        if old_position_higher:
            CW_new[v] = n_right - n_left + cw_old
        else:
            CW_new[v] = n_left - n_right + cw_old
        return CW_new

    def compute_new_cutwidth_for_all_vertices(self, CW, f_old, f_new, vertex, old_position, new_position):
        CW_new = CW.copy()

        if new_position < old_position:
            for i in range(new_position + 1, old_position + 1):
                CW_new = self.recompute_cutwidth_for_inserted_vertices(CW_new, f_old, f_new, vertex, i, True)
            if new_position == 1:
                CW_new.pop(vertex)
                CW[vertex] = len(self.graph.neighbors(f_new[new_position]))
            else:
                CW_new = self.recompute_cutwidth_for_one_vertex(CW_new, f_new, vertex, new_position, True)

        elif new_position > old_position:
            for i in range(old_position, new_position):
                CW_new = self.recompute_cutwidth_for_inserted_vertices(CW_new, f_old, f_new, vertex, i, False)
            if new_position == len(f_new):
                CW_new.pop(vertex)
                CW_new[vertex] = 0
            else:
                CW_new = self.recompute_cutwidth_for_one_vertex(CW_new, f_new, vertex, new_position, False)

        # print 'CW_new: ' + str(CW_new)
        return CW_new

    def compute_cutwidth_by_labeling(self, graph, f):
        CW = {}
        for i in range(1, len(f) + 1):
            if i == 1:
                CW[f[i]] = len(graph.neighbors(f[i]))
            else:
                n_left, n_right = self.get_left_right_neigbors(graph, f, f[i], i)
                CW[f[i]] = CW[f[i-1]] + n_right - n_left
        return CW

    # parameters: BETA, CW
    def get_critical_vertices(self, CW):
        BETA = 0.5
        CV = {}
        restriction = round(BETA * self.dv.get_cutwidth_of_graph(CW))
        for v in CW:
            if CW[v] >= restriction:
                if CW[v] in CV:
                    CV[CW[v]].append(v)
                else:
                    CV[CW[v]] = [v]

        # print 'restrinction ' + str(restriction)
        # print 'CV: ' + str(CV)
        return CV

    def is_improve(self, CW_G, CW_G_new):

        if CW_G < CW_G_new:
            return True
            # else:
            # CV_new = self.get_critical_vertices(CW_new)
            # keys_sorted = sorted(CV.keys(), reverse=True)
            # keys_sorted_new = sorted(CV_new.keys(), reverse=True)
            #
            # for k in keys_sorted:
            #     if k in keys_sorted_new:
            #         if len(CV_new[k]) < len(CV[k]):
            #             return True
        return False

    # parameters: graph, f, pos, v
    def move(self, f, pos, v):
        # print 'Labeling(f): ' + str(f)
        labeling_v = self.get_label_by_vertex(f, v)
        if labeling_v == pos:
            return f

        f.pop(labeling_v)
        if pos < labeling_v:
            f_new = self.update_dict(f, pos, labeling_v - 1, reverse=True)
        else:
            f_new = self.update_dict(f, labeling_v + 1, pos)
        f_new[pos] = v
        return f_new

    def improvement(self, f, CW, CW_G):

        f_temp = {}
        CW_temp = {}
        CW_G_temp = CW_G
        # print "CW_G origin: " + str(CW_G)

        CV = self.get_critical_vertices(CW)
        keys_sorted = sorted(CV.keys(), reverse=True)

        for k in keys_sorted:
            for vertex in CV[k]:

                neighbors = self.graph.neighbors(vertex)
                neighbors = map(int, neighbors)
                median = int(round(np.median(neighbors)))

                old_position = self.get_label_by_vertex(f, vertex)
                f_new = self.move(f.copy(), median, vertex)
                CW_new = self.compute_new_cutwidth_for_all_vertices(CW, f, f_new, vertex, old_position,
                                                                    median)
                CW_G_new = self.dv.get_cutwidth_of_graph(CW_new)

                if CW_G_new < CW_G_temp:
                    f_temp = f_new
                    CW_temp = CW_new
                    CW_G_temp = CW_G_new

        if len(f_temp) > 0:
            f = f_temp
            CW = CW_temp
            CW_G = CW_G_temp

        print 'CW_G_new: ' + str(CW_G)
        return f, CW, CW_G

    # def create_test_graph(selg):
    #     letters = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "6": "F"}
    #     print letters
    #     g = nx.Graph()
    #     g.add_edge(1, 2)
    #     g.add_edge(1, 4)
    #     g.add_edge(1, 5)
    #     g.add_edge(2, 1)
    #     g.add_edge(2, 3)
    #     g.add_edge(3, 2)
    #     g.add_edge(4, 1)
    #     g.add_edge(4, 5)
    #     g.add_edge(4, 6)
    #     g.add_edge(5, 1)
    #     g.add_edge(5, 4)
    #     g.add_edge(5, 6)
    #     g.add_edge(6, 4)
    #     g.add_edge(6, 5)
    #     return g, letters
    #
    # def test(self):
    #     print '-----------'
    #     print self.get_f_with_letters(self.f, self.letters)
    #     print 'CW: ' + str(self.get_f_with_letters(self.CW, self.letters, cw=True))
    #     self.improvement()
    #     print self.get_f_with_letters(self.f, self.letters)
    #     print 'CW_new: ' + str(self.get_f_with_letters(self.CW, self.letters, cw=True))
    #
    # def get_f_with_letters(self, f, letters, cw=False):
    #     f_with_letters = {}
    #     if cw:
    #         for i in f:
    #             f_with_letters[letters[str(i)]] = f[i]
    #     else:
    #         for i in f:
    #             f_with_letters[i] = letters[str(f[i])]
    #     return f_with_letters
