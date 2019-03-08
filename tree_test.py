import dtree_build
import sys
import csv
import dtree_draw

def build(csv_file_name, attributes):

    data = []
    labels=True
    with open(csv_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if labels:
                col_names=row
                labels=False
            else:
                op=list(row)
                for i in range(len(op)):
                    if attributes[col_names[i]][0]=='n':
                        op[i]=float(op[i])
                data.append(op)

    print("Total number of records = ",len(data))
    tree = dtree_build.buildtree(data, min_gain =0.01, min_samples = 5)
    dtree_build.printtree(tree, '', col_names)

    max_tree_depth = dtree_build.max_depth(tree)
    print("max number of questions=" + str(max_tree_depth))
    
    dtree_draw.drawtree(tree, jpeg=csv_file_name+'.jpg')
    
    return tree
   
    '''csv_predict="predict.csv"
    predict=[]
    with open(csv_file_name) as csvpredict:
        CSVp = csv.reader(csv_predict, delimiter=',')
        for row in CSVp:
            predict.append(list(row))
    print(regression_tree.classify(predict,tree))'''

if __name__ == "__main__":
    col_names = []
    main(col_names)

