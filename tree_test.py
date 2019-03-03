import dtree_build
import sys
import csv


def main(col_names=None):
    # parse command-line arguments to read the name of the input csv file
    # and optional 'draw tree' parameter
    if len(sys.argv) < 2:  # input file name should be specified
        print ("Please specify input csv file name")
        return

    csv_file_name = sys.argv[1]

    data = []
    labels=True
    with open(csv_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if labels:
               col_names=row
               labels=False
            else:
                data.append(list(row))

    print("Total number of records = ",len(data))
    tree = dtree_build.buildtree(data, min_gain =0.01, min_samples = 5)
    dtree_build.printtree(tree, '', col_names)

    max_tree_depth = dtree_build.max_depth(tree)
    print("max number of questions=" + str(max_tree_depth))

    if len(sys.argv) > 2: # draw option specified
        import dtree_draw
        dtree_draw.drawtree(tree, jpeg=csv_file_name+'.jpg')

if __name__ == "__main__":
    col_names = []
    main(col_names)





