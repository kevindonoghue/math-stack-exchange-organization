"""
The math.stackexchange database is downloaded as a set of xml files. This script converts them to a SQL database.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from xml_to_sql_classes import Base, Badge, Comment, Post, PostRecord, PostLink, Tag, User, Vote
import time


db = 'sqlite:///../mse.db'


engine = create_engine(db)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

classes = {'Badges.xml': Badge,
           'Comments.xml': Comment,
           'Posts.xml': Post,
           'PostHistory.xml': PostRecord,
           'PostLinks.xml': PostLink,
           'Tags.xml': Tag,
           'Users.xml': User,
           'Votes.xml': Vote}

def add_table(name, limit=None):
    with open('../xml/' + name) as f:
        print(f'calculating length of {name}')
        length = 0
        for line in f:
            length += 1
    start_time = time.time()
    with open('../xml/' + name) as f:
        i = 0
        for line in f:
            x = classes[name].parse_line(line)
            if x:
                session.add(x)
            if i % 10000 == 0 and i != 0:
                session.commit()
                est_time = (length - i)/(i/(time.time()-start_time))
                if est_time < 60:
                    est_time = '<1 min'
                else:
                    est_time = f'{int(est_time // 60)} min'
                print(f'{name} line {i}/{length}, estimated time remaining: {est_time}')
            i += 1
            if limit != None and i > limit:
                break
            
    session.commit()
            
