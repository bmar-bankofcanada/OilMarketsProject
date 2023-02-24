#Slice by Paragraph 
from distutils.file_util import write_file
import json
import pandas as pd

def split_by_paragraph(file_name):
    new_json = []
    with open(f"data/{file_name}.json","r") as file:
        data = json.load(file)
        for article in data['data']:
            new_texts = article['text'].split('\n')
            for new_text in new_texts:
                if len(new_text) > 5:
                    item = {
                        "title":article['title'],
                        "text":new_text,
                        "section":article['section'],
                        "categories":article['categories'],
                        "date":article['date']}
                    new_json.append(item)
    with open(f"data/paragraph_{file_name}.json",'w') as file:
        json.dump(new_json,file,indent=2)

def shuffle_json(json_name):
    #"./data/market_prices.json"
    df = pd.read_json(f"data/{json_name}.json",convert_dates=False)
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_json(f"data/shuffle_{json_name}.json",orient="records",indent=2)

def get_500(json_name,start=0,end=500):
    with open(f"data/{json_name}.json",'r') as file:
        data = json.load(file)
        with open(f"data/500_{json_name}.json",'w+') as to_write:
            new_json = []
            for i in range(start,end):
                new_json.append(data[i])
            json.dump(new_json,to_write,indent=2)