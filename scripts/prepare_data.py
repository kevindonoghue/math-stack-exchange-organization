from xml_to_sql_migration import add_table, classes
from tokenize_data import tokenize

# for class_ in classes:
#     add_table(class)

add_table('Posts.xml', 1000)
tokenize()
