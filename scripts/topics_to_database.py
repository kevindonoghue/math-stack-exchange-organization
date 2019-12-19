import numpy as np
import pandas as pd
import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('num_levels', type=int)
args = parser.parse_args()
num_levels = args.num_levels

db = 'sqlite:///../data/mse.db'

document_topics = pd.DataFrame([], list(range(num_levels)), dtype=int)

def get_idx_and_topic_from_line(line):
    arr = line.split()
    idx = int(arr[1].split('/')[-1][:-4])
    topic_weights = np.array(list(map(float, arr[2:])))
    topic = np.argmax(topic_weights)
    return idx, topic

def get_topics(level=0, current_dir='../records'):
    with open(os.path.join(current_dir, 'input_document_topics.txt')) as f:
        for line in f:
            idx, topic = get_idx_and_topic_from_line(line)
            document_topics.loc[idx, level] = topic
        i = 0
        while str(i) in os.listdir(current_dir):
            get_topics(level+1, os.path.join(current_dir, str(i)))
            i += 1
 
def get_topic_descriptions(current_dir='../records'):
    if not os.path.exists(current_dir):
        return []

    with open(os.path.join(current_dir, 'topic_key.txt')) as f:
        return_arr = []
        for i, line in enumerate(list(f)):
            topic = {'description': line.split('\t')[2].strip('\n'),
                     'children': get_topic_descriptions(current_dir=os.path.join(current_dir, str(i)))}
            return_arr.append(topic)
            
    return return_arr

get_topics()
document_topics.to_sql('document_topics', db, index=True, if_exists='replace')

topic_descriptions = get_topic_descriptions()
with open('../data/topic_descriptions.json', 'w+') as f:
    json.dump(topic_descriptions, f)