#! /bin/bash


let num_levels=3
let num_topics=4
let num_iterations=500

# get documents for first level
python3 get_initial_documents.py

# run train_helper.sh, which recursively calls itself at each level
# arguments are temp_dir, record_dir, nun_levels, num_topics, num_iterations
echo "starting to train"
bash train_helper.sh ../temp ../records $num_levels $num_topics $num_iterations

# delete temp folder
echo "cleaning up"
rm -r ../temp

# convert data in records to a database table containing the topics for each post and a json file containing the topic descriptions
echo "copying topic data to database and setting up topic_descriptions.json"
python3 topics_to_database.py $num_levels
