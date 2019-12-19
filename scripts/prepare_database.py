import os
from xml_to_sql_migration import add_table, classes
from tokenize_data import tokenize


for class_ in classes:
    add_table(class_, 1000)

tokenize()
