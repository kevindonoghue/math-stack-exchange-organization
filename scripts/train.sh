#! /bin/bash


# get documents for first level
python3 get_initial_documents.py

# run train_helper.sh, which recursively calls itself at each level
# arguments are temp_dir, record_dir, nun_levels, num_topics, num_iterations
echo "starting to train"
bash train_helper.sh ../temp ../records 2 3 50

echo "cleaning up"
rm -r ../temp