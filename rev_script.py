import sys
import csv
import math
import random
import tree_test
import dtree_build
import naive_pdf

attributes={'TOTAL_VISITS':'n','TOTAL_SPENT':'n','AVRG_SPENT_PER_VISIT':'n',
        'HAS_CREDIT_CARD':'s',"PSWEATERS":'n', "PKNIT_TOPS":'n', "PKNIT_DRES":'n', "PBLOUSES":'n', 
        "PJACKETS":'n', "PCAR_PNTS":'n', "PCAS_PNTS":'n', "PSHIRTS":'n',"PDRESSES":'n', "PSUITS":'n', 
        "POUTERWEAR":'n', "PJEWELRY":'n', "PFASHION":'n', "PLEGWEAR":'n', "PCOLLSPND":'n',"AMSPEND":'f',
        "PSSPEND":'f',"CCSPEND":'f',"AXSPEND":'f','GMP':'n','PROMOS_ON_FILE':'n','FREQ_DAYS':'n',
        'MARKDOWN':'n',
        'PRODUCT_CLASSES':'n','COUPONS':'n','STYLES':'n','STORES':'c',
        'VALPHON':'s','WEB':'s','MAILED':'n','RESPONDED':'n','RESPONSERATE':'n',
        'LTFREDAY':'n','CLUSTYPE':'d','PERCRET':'n','RESP':'s'}

p_series=["PSWEATERS","PKNIT_TOPS", "PKNIT_DRES", "PBLOUSES", "PJACKETS",
        "PCAR_PNTS", "PCAS_PNTS", "PSHIRTS","PDRESSES", "PSUITS", "POUTERWEAR",
        "PJEWELRY","PFASHION", "PLEGWEAR", "PCOLLSPND"]

bins = {"TOTAL_VISITS": [1, 2, 5, 10, 20], "TOTAL_SPENT": [0, 100, 400, 1000, 2000],
        "AVRG_SPENT_PER_VISIT": [0, 50, 150, 300], "PCLOTHING": [0, 0.05, 0.3, 0.5, 0.7],
        "GMP": [0, 0.5, 0.6], "PROMOS_ON_FILE": [0, 5, 15, 25], "FREQ_DAYS": [0, 50, 150, 300],
        "MARKDOWN": [0, 0.1, 0.25, 0.4], "PRODUCT_CLASSES": [0, 4, 10, 20],"STYLES": [0, 5, 15, 30],
        "MAILED": [0, 3, 5, 8], "RESPONDED": [0, 0.1, 1, 3, 6], "RESPONSERATE": [0, 0.1, 1, 25, 50, 75],
        "LTFREDAY": [0, 40, 80, 150], "PERC_RET": [0, 0.000001, 0.1, 0.4, 0.8]}

def main():
    if len(sys.argv) < 2:  # input file name should be specified
        print ("Please specify input csv file name")
        return

    global attributes
    csv_file_name = sys.argv[1]
    
    data = []
    columns=[]

    labels=True
    clus=['10','1','4','16','8','15']

    with open(csv_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if labels:
                col_names=row
                labels=False
            else:
                data.append(list(row))
    n_list=[]
    for m in range(len(data)):
        for n in range(len(data[0])):
            func=attributes[col_names[n]]

            if (func=='d'):
                data[m][n]=str(data[m][n])
                if data[m][n] not in clus:
                    data[m][n]='other'
                   
            elif (func=='n'):
                data[m][n]=float(data[m][n])
                
                name=col_names[n]
                        
                if name in bins:
                    for j in range(1, len(bins[name])):
                        if data[m][n] <= bins[name][j]:
                            data[m][n]=bins[name][j-1]
                            break
                        elif j==len(bins[name])-1:
                            data[m][n]=bins[name][-1]

                elif name in p_series:
                    for j in range(1, len(bins["PCLOTHING"])):
                        if data[m][n] <= bins["PCLOTHING"][j]:
                            data[m][n]=bins["PCLOTHING"][j-1]
                            break
                        elif j==len(bins["PCLOTHING"])-1:
                            data[m][n]=bins["PCLOTHING"][-1]

                if name=='COUPONS':
                    if data[m][n]<=3:
                        data[m][n]=3
                    else:
                        data[m][n]=4
                elif name=='STORES':
                    if data[m][n]<=4:
                        data[m][m]=4
                    else:
                        data[m][n]=5

            elif (func=='f'):
                if data[m][n]=='0':
                    data[m][n]='N'
                else:
                    data[m][n]='Y'
    
   # print(data)
    f_name='discretized_data.csv'
    with open(f_name,'w') as csvfile:
        writer=csv.writer(csvfile, delimiter=',',lineterminator='\n')
        writer.writerow(col_names)
        for i in data:
            writer.writerow(i)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def tree(f_name):
    global attributes
    n_tree=tree_test.build(f_name, attributes)
    print (n_tree)

def pdf(f_name):
    global attributes
    naive_pdf.build(f_name, attributes)

def bootstrap(f_name):
    global attributes
    data=[]
    new=[]
    total=0
    labels=True

    with open(f_name) as csvfile:
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
                total+=1

    new.append(col_names)
    for i in range(total):
        num=random.randint(0,total-1)
        new.append(data[num])
    with open('test_dataset.csv','w') as csvfile:
        writer=csv.writer(csvfile, delimiter=',',lineterminator='\n')
        for i in new:
            writer.writerow(i)
    
def accuracy(f_name):
    global attributes
    total=0
    labels=True
    data=[]
    d_tree_p=[]
    n_bayes_p=[]
    real=[]
    
    with open('test_dataset.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if labels:
                col_names=row
                labels=False
            else:
                real.append(int(row[-1]))
                op=list(row)
                for i in range(len(op)):
                    if attributes[col_names[i]][0]=='n':
                        op[i]=float(op[i])
                data.append(op)
                total+=1
    
    pdf(f_name) 
    n_bayes_p=naive_pdf.classifier(data)
    tree=tree_test.build(f_name, attributes)
    print("tree built")
    # save the classifier
    d_tree_p=dtree_build.test_classify(tree, data) 
    print("tree results")
    d_percent=0
    n_percent=0
    lift=[[],[],[],[],[]] # [letters][rand_pos][confidence][actual positives]
    count=0
    for i in range(total):
        count+=1
        pos=0
        rand_pos=0
        if real[i]==1:
            rand_pos=1
        #if (real[i]==1 and d_tree_p[i]==real[i]):
        if ((d_tree_p[i]>real[i] and real[i]==1) or (real[i]==0 and d_tree_p[i]==0)):    
            d_percent+=1
        #if (real[i]==1 and n_bayes_p[i]==real[i]):
        if (n_bayes_p[i]==real[i]):
            n_percent+=1
        if (i<2000):
            lift[0].append(count)
            lift[1].append(rand_pos)

        if (d_tree_p[i]>0):
            if (real[i]==1):
                pos=1
            lift[2].append(d_tree_p[i])
            lift[3].append(pos)
     
    #lift.sort(key=compare, reverse=True)
    #d_tree_p.sort(key=compare, reverse=True)
    '''pos_b=0
    pos_r=0
    for i in lift:
        if i[1]==1:
            pos_b+=1
        if i[2]==1:
            pos_r+=1
        i.append(pos_b)
        i.append(pos_r)'''

    with open('results.csv','w') as csvfile:
        writer=csv.writer(csvfile, delimiter=',',lineterminator='\n')
        for i in lift:
            writer.writerow(i)

    #print(n_percent) 
    d_percent/=total
    n_percent/=total
    print("decision tree accuracy: "+str(round(d_percent*100,2))+
            " and "+"naive bayes: "+str(round(n_percent*100,2)))

def compare(nums):
    return nums[0]

if __name__=='__main__':
    main()
