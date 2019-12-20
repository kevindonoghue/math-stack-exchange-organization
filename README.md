1. Extract https://archive.org/download/stackexchange/mathematica.stackexchange.com.7z to `./xml`.

2. Run `bash setup.sh` to produce a data folder that contains 1) mse.db, a database with the posts and their topics, and topic_descriptions.json, a json file with descriptions of the topics.

3. You can change the number of topics, number of levels, and number of LDA training iterations in `scripts/train.sh`.