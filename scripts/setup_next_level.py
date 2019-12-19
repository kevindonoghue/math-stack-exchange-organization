"""
called in train_helper.sh to copy documents to next level
"""


import numpy as np
import shutil
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('temp_dir', type=str)
parser.add_argument('records_dir', type=str)
parser.add_argument('num_topics', type=int)

args = parser.parse_args()
temp_dir = args.temp_dir
records_dir = args.records_dir
num_topics = args.num_topics

for i in range(num_topics):
    os.makedirs(os.path.join(temp_dir, str(i), 'documents'), exist_ok=True)
    os.makedirs(os.path.join(records_dir, str(i)), exist_ok=True)

with open(os.path.join(records_dir, 'input_document_topics.txt')) as f:
    for line in f:
        arr = line.split()
        idx = int(arr[1].split('/')[-1][:-4])
        topic_weights = np.array(list(map(float, arr[2:])))
        topic = np.argmax(topic_weights)
        shutil.copyfile(os.path.join(temp_dir, 'documents', str(idx) + '.txt'),
                        os.path.join(temp_dir, str(topic), 'documents', str(idx) + '.txt'))
