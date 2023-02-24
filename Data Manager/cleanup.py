import csv

labels = [
    '__label__Not Relevant',
    '__label__Prices Positive',
    '__label__Prices Negative',
    '__label__Supply Positive',
    '__label__Supply Negative',
    '__label__Demand Positive',
    '__label__Demand Negative',
    '__label__Intermediate',
    '__label__Future',
    '__label__Current',
    '__label__Uncertain Label',
    '__label__Prices Neutral',
    '__label__Supply Neutral',
    '__label__Demand Neutral'
]
clean_up = "__label__"
new_csv = []

with open("data/all.txt",'r') as my_file:
    for line in my_file:
        text_labels = ''
        for label in labels:
            if len(line.split(label)) > 1:
                line = line.split(label)[1]
                text_labels = text_labels + "#" + label.split(clean_up)[1]
        new_csv.append({'data':line.strip(),'labels':text_labels[1:]})
    
#write CSV
with open('data/oil_category_2.csv','w') as csv_file:
    writer = csv.DictWriter(csv_file,fieldnames=['data','labels'],delimiter="|")
    writer.writeheader()
    writer.writerows(new_csv)