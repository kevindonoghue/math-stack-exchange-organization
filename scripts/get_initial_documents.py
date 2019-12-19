"""
The Mallet implementation of LDA takes as input a folder of documents. This creates such a folder from the database.
"""


import pandas as pd
import os



db = f'sqlite:///../mse.db'


print('getting initial document files')

os.makedirs('../records')

query = \
"""
SELECT id, augmented_body_text AS text FROM preprocessed_text
"""

text_data = pd.read_sql_query(query, db, index_col='id')

def condition(x):
    return all([
        not x.isnumeric(),
        len(x) > 1,
        x not in ('align', 'begin_align', 'end_align', 'left', 'right',
                'end_array', 'begin_array', 'quad', 'qquad', 'eqnarray',
                'tag', 'displaystyle', 'array', 'begin_array',
                'end_array', 'mathbb', 'mathcal', 'mathbf', 'begin')
    ])
    
    
os.makedirs(f'../temp/documents/', exist_ok=True)
for idx in text_data.index:
    new_body = ' '.join([x for x in text_data.loc[idx, 'text'].split() if condition(x)])
    with open(f'../temp/documents/{idx}.txt', 'w+') as f:
        f.write(new_body)