import sys
import csv
import math

results=[] # per row: if str: ['s', P(0|YES),P(0|NO),p(1|yes),p(1|no)] 
#if num: ['n', mean(Y), variance(Y), mean(N), variance(N), n(yes),n(no)]
total=0
y_n=[0,0]

def build(csv_file_name, attributes):
    global results
    global total

    col_names=[]

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
                    if attributes[col_names[i]]=='n':
                        op[i]=float(op[i])

                yes_no(op[-1])
                data.append(op)
                total+=1 # number of rows

    #print(data[0])
    cols=len(data[0])-1
    for i in range(cols):
        if (type(data[0][i])==str):
            results.append(['s',0,0,0,0])
        else:
            results.append(['n',0,0,0,0,0,0])
    #print(results) 
    mean_and_str(data)
    variance(data)
    # print(results)
    # classifier()

def classifier(p_data):
    global results
    global total

    cols=len(p_data[0])-1
    classified=[]
    target=[]
    for row in p_data:
        y=1
        n=1
        for i in range(cols):
            if results[i][0]=='s':
                if (row[i]=='0'):
                    y*=results[i][1]
                    n*=results[i][2]
                else:
                    y*=results[i][3]
                    n*=results[i][4]
            else:
                y_mean=results[i][1]
                n_mean=results[i][3]
                y_v=results[i][2]
                n_v=results[i][4]
                
                #print(str(results[i])+" column "+str(i))
                y*=1/(math.sqrt(y_v*2*math.pi))*pow(math.e,-((pow((row[i]-y_mean),2))/(2*y_v)))
                # plug in equation
                n*=1/(math.sqrt(n_v*2*math.pi))*pow(math.e,-((pow((row[i]-n_mean),2))/(2*n_v)))
                
        y*=(y_n[0]/total)
        n*=(y_n[1]/total)
        if (y>n):
            target.append(1)
        else:
            target.append(0)
    
    return target

def write(p_data):
    
    with open('naive_results.csv','w') as csvfile:
        writer=csv.writer(csvfile, delimiter=',',lineterminator='\n')
        for i in p_data:
            writer.writerow(i)

def yes_no(target):
    global y_n

    if target=='1':
        y_n[0]+=1
    else:
        y_n[1]+=1

def mean_and_str(data):
    global results
    global y_n
    global total

    cols=len(data[0])-1

    for i in range(cols): # do columns not rows
        
        if (results[i][0]=='s'):
            col_type='str'
        else:
            col_type='num'

        for j in range(total):
            if (col_type=='str'):
                if ((data[j][i]=='0' or data[j][i]=='N') and data[j][-1]=='1'):
                    results[i][1]+=1
                elif ((data[j][i]=='0' or data[j][i]=='N') and data[j][-1]=='0'):
                    results[i][2]+=1
                elif ((data[j][i]=='1' or data[j][i]=='Y') and data[j][-1]=='1'):
                    results[i][3]+=1
                elif ((data[j][i]=='1' or data[j][i]=='Y') and data[j][-1]=='0'):
                    results[i][4]+=1

            else: # col_type=int or float
                if data[j][-1]=='0':
                    results[i][3]+=data[j][i] # mean(no)
                    results[i][6]+=1 # n(no)
                else: # target=1
                    results[i][1]+=data[j][i] # mean(yes)
                    results[i][5]+=1 # n(yes)
        if col_type=='num':
            results[i][3]/=results[i][6] # mean(n)/n(no)
            results[i][1]/=results[i][5] # mean(y)/n(yes)
        else:
            results[i][1]/=y_n[0] # P(0|y)
            results[i][3]/=y_n[1] # P(0|n)
            results[i][2]/=y_n[0] # P(1|y)
            results[i][4]/=y_n[1] # P(1|n)

def variance(data):
    global results
    global total

    cols=len(data[0])-1

    for i in range(cols): # do columns not rows
        
        if (results[i][0]=='s'):
            is_num=False
        else:
            is_num=True
        
        if is_num==False:
            continue

        for j in range(total):
            if data[j][-1]=='0':
                mean=results[i][3]
                results[i][4]+=pow((data[j][i]-mean),2) # variance(no)
            else: # target=1
                mean=results[i][1]
                results[i][2]+=pow((data[j][i]-mean),2) # variance(yes)
        
        results[i][4]/=(results[i][6]-1) # v(n)/n-1(n)
        results[i][2]/=(results[i][5]-1) # v(y)/n-1(y)

if __name__=='__main__':
    main()
