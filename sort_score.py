import csv
import json

locations={}
with open("locations_classified.tsv", encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    for row in readCSV:
        line=list(row)
        lat=line[0]
        long=line[1]
        if (lat,long) not in locations:
            locations[lat,long]=[0,0]
        locations[lat,long][0]+=1

with open("locations_classified.tsv", encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    for row in readCSV:
        line=list(row)
        lat=line[0]
        long=line[1]
        mood=line[2]
        if mood=="positive":
            locations[lat,long][1]+=1
        elif mood=="negative":
            locations[lat,long][1]-=1
adjusted=[]
for i in locations:
    #print(i)
    locations[i][1]=((locations[i][1]/locations[i][0])+1)/2
    geo=list(i)
    geo.append(locations[i][1])
    adjusted.append(geo)

'''with open('locations_scored.tsv', 'w') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t',lineterminator='\n')
        for i in adjusted:
            writer.writerow(i)'''
data=[]
for i in adjusted:
    #print(i)
    i[0]=round(float(i[0])+0.05/2,2)
    i[1]=round(float(i[1])+0.05/2,2)
    data.append({'score':round(i[2],2), 'g':i[1],'t':i[0]})

with open('data.js', 'w') as outfile:  
    json.dump(data, outfile)
#print(locations)
#print(graph)

    