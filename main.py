import ScatterSearch as ss


def main():
    graphs_name = ["small_p100.txt", "hardwell_will199.txt", "hardwell_fs680.txt", "hardwell_dwt592.txt",
                   "hardwell_west0655.txt"]

    for i in range(0, len(graphs_name)):
        print 'FILE NAME: ' + graphs_name[i] + '\n'
        ss.scatter_search(graphs_name[i])
        print "-----------------------"
        print '\n'


main()
