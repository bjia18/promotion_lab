import csv
import math

word_counts_dict = {}
classifier={}
categories=["positive", "negative","neutral", "irrelevant"]
c_counts=[0,0,0,0]
with open("labeled_corpus.tsv", encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    for row in readCSV:
        line_arr = list(row)

        tweet = line_arr[0]
        category=line_arr[1]
        for i in range(4):
            if (category==categories[i]):
                c_counts[i]+=1

        words = tweet.split()
        word_set = set()
        for w in words:
            if '#' not in w and '@' not in w:
                word_set.add(w)

        for w in word_set:
            if w not in word_counts_dict:
                word_counts_dict[w] = 0
            word_counts_dict[w] += 1

# create list of tuples to sort
word_freq_sorted = []
words_counted=[]
total=0
for w,count in word_counts_dict.items():
    if count > 1:
        word_freq_sorted.append((count,w))
for count,w in word_freq_sorted:
    words_counted.append(w)

with open("labeled_corpus.tsv", encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    for row in readCSV:
        total+=1
        line_arr = list(row)

        tweet = line_arr[0]
        category=line_arr[1]
        
        words = tweet.split()
        word_set = set()
        for w in words:
            if '#' not in w and '@' not in w:
                word_set.add(w)
        for w in words_counted:
            if w in word_set:
                if w not in classifier:
                    classifier[w]=[0,0,0,0]
                for i in range (4):
                    if (categories[i]==category):
                        classifier[w][i]+=1

for w in classifier:
    for i in range(4):
        classifier[w][i]=classifier[w][i]/c_counts[i]
print(c_counts)
#print(classifier)
classifications=[]

with open ('geo_twits_squares.tsv',encoding="utf-8") as csvfile:
    #csvfile=csvfile.replace('\0', '')
    readCSV = csv.reader((line.replace('\0','') for line in csvfile),delimiter='\t')

    '''data=csvfile.read()
    print (data.find('\x00'))'''
    for row in readCSV:
        results={"positive":0,"negative":0,"neutral":0,"irrelevant":0}
        for i in range(4):
            results[categories[i]]=math.log2(c_counts[i]/total)
        line_arr = list(row)
        lat=line_arr[0]
        long=line_arr[1]
        tweet = line_arr[2]
        words = tweet.split()
        word_set = set()
        for w in words:
            if '#' not in w and '@' not in w and w in classifier:
                word_set.add(w)
        for w in word_set:
            for i in range (4):
                #print(classifier[w][i])
                if classifier[w][i]!=0:
                    results[categories[i]]+=math.log2(classifier[w][i])
        max=results[categories[0]]
        for i in range (4):
            if results[categories[i]]>max:
                max=results[categories[i]]
        final=list(results.keys())[list(results.values()).index(max)]
        classifications.append((lat,long,final))

with open('locations_classified.tsv', 'w') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t',lineterminator='\n')
        for i in classifications:
            writer.writerow(i)
#print(classifications)

#print(classifier)
#print(words)
'''word_freq_sorted.sort()
print(word_freq_sorted)

word_freq_sorted.reverse()
print(word_freq_sorted)

print(len(word_freq_sorted))'''