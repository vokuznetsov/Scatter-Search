import Improvement
import numpy as np
import networkx as nx


def main():
    graphs_name = ["small_p100.txt", "hardwell_will199.txt", "hardwell_fs680.txt", "hardwell_dwt592.txt",
                   "hardwell_west0655.txt"]

    im = Improvement.Improvement(graphs_name[1])
    f, CW, CW_G = im.improvement()
    print 'Labeling: ' + str(f)
    print 'Cutwidth of vertices: ' + str(CW)
    print 'Cutwidth of graph: ' + str(CW_G)

    # im.test()

main()
