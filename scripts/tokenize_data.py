"""
called in prepare.sh to tokenize texts in math.stackexchage database
"""


import numpy as np
import pandas as pd
import re
import html
from tqdm import tqdm

from gensim.models import Phrases
from gensim.parsing.preprocessing import remove_stopwords

from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

db = 'sqlite:///../mse.db'

def tokenize():

    # database --> pandas dataframe
    query = \
    """
    SELECT id, body, title, tags
    FROM post
    """
    data = pd.read_sql_query(query, db, index_col='id')


    # some helper functions
    tag_re = re.compile(r'<[^>]+>')
    def handle_html(s):
        return html.unescape(tag_re.sub('', s))
    
    def fix_body_or_title(s):
        if not s:
            return ''
        s = handle_html(s)
        s = (s.lower()
            .replace('<', ' < ')
            .replace('>', ' > ')
            .replace('$', ' ')
            .replace('_', ' ')
            .replace('{', ' ')
            .replace('}', ' ')
            .replace('^', ' ')
            .replace('*', ' ')
            .replace('(', ' ')
            .replace(')', ' ')
            .replace('[', ' ')
            .replace(']', ' ')
            .replace(':', ' : '))
        s = remove_stopwords(s)
        return s

    def fix_tags(s):
        if not s:
            return ''
        s = (s.lower()
            .replace('<', ' ')
            .replace('>', ' '))
        return s


    # tokenizer and lemmatizer
    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()


    # process body, title and tags and save them in a table in the database
    try:
        empty_df = pd.DataFrame(columns=['id', 'body', 'title', 'tags'])
        empty_df.to_sql('preprocessed_text', db)
    except:
        pass
        
    for idx in tqdm(data.index):
        body = fix_body_or_title(data.loc[idx, 'body'])
        title = fix_body_or_title(data.loc[idx, 'title'])
        tags = fix_tags(data.loc[idx, 'tags'])
        body = [lemmatizer.lemmatize(x) for x in tokenizer.tokenize(body)]
        title = [lemmatizer.lemmatize(x) for x in tokenizer.tokenize(title)]
        tags = tags.split()

        body = ' '.join(body)
        title = ' '.join(title)
        tags = ' '.join(tags)
        temp_df = pd.DataFrame({'id': [idx], 'body': [body], 'title': [title], 'tags': [tags]})

        temp_df.to_sql('preprocessed_text', db, if_exists='append', index=False)
        
        
    # retrieve the preprocessed body, title and tags
    preprocessed_query = \
    """
    SELECT * FROM preprocessed_text
    """
    data_preprocessed = pd.read_sql_query(preprocessed_query, db, index_col='id')


    # look for bigrams in the body counts
    # combine body title, body text, bigrams, and tags together in a column called augmented_body_text
    # need to process bigrams in groups due to memory limitations
    data_preprocessed['augmented_body_text'] = pd.Series()
    sub_indices = np.array_split(data_preprocessed.index, 5)
    for sub_index in sub_indices:
        print(f'processing indices from {sub_index[0]} to {sub_index[-1]}')
        body_docs = [x.split() for x in data_preprocessed.loc[sub_index, 'body']]
        print('processing bigrams...')
        bigram = Phrases(body_docs, min_count=20)
        for i, x in tqdm(enumerate(bigram[body_docs])):
            for token in bigram[x]:
                if '_' in token:
                    body_docs[i].append(token)
            body_docs[i] = ' '.join(body_docs[i])
        ser = pd.Series(body_docs, index=sub_index)
        data_preprocessed['augmented_body_text'] = ser.combine_first(data_preprocessed['augmented_body_text'])
        
    data_preprocessed.to_sql('preprocessed_text', db, index=True, if_exists='replace')