#! /bin/bash

temp_dir="$1"
records_dir=$2
num_levels="$3"
num_topics="$4"
num_iterations="$5"

echo $num_levels

if [ $num_levels != 0 ]
then


# encode folder of documents into mallet format
echo "importing documents"
../mallet-2.0.8/bin/mallet import-dir --input $temp_dir/documents --output $temp_dir/encoded_data.mallet --keep-sequence

# train the model, output topic key and input topics to record_dir
echo "training"
../mallet-2.0.8/bin/mallet train-topics --input $temp_dir/encoded_data.mallet --num-iterations $num_iterations --num-topics $num_topics --optimize-interval 20 --num-threads 7 --output-topic-keys $records_dir/topic_key.txt --output-doc-topics $records_dir/input_document_topics.txt --inferencer-filename $records_dir/inferencer

# set up new directories in temp_dir and records_dir
echo "copying documents"
if [ $num_levels != 1 ]
then
python3 setup_next_level.py $temp_dir $records_dir $num_topics
fi

# call again for each topic
let next_num_levels=$num_levels-1
for ((i=0; i<$num_topics; i+=1))
do
bash train_helper.sh $temp_dir/$i $records_dir/$i $next_num_levels $num_topics $num_iterations
done


fi