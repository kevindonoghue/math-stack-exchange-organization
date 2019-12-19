"""
sqlalchemy classes used in setting up the database in xml_to_sql_migration
"""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from bs4 import BeautifulSoup


def string_to_dt(s):
    if s == None:
        return
    return datetime.datetime.strptime(s, r"%Y-%m-%dT%H:%M:%S.%f")

def int_conv(x):
    if x == None:
        return
    return int(x)


Base = declarative_base()

class Badge(Base):
    __tablename__ = 'badge'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String(250))
    date = Column(DateTime)
    class_ = Column(Integer)
    tag_based = Column(Boolean)
    
    @classmethod
    def parse_line(cls, line):
        x = line.strip()
        if x[1:4] != 'row':
            return
        d = BeautifulSoup(x, 'xml').find('row').attrs
        
        for label in ('Id', 'UserId', 'Name', 'Date', 'Class', 'TagBased'):
            if label not in d:
                d[label] = None
                
        return Badge(id=int_conv(d['Id']),
                     user_id=int_conv(d['UserId']),
                     name=d['Name'],
                     date=string_to_dt(d['Date']),
                     class_=int_conv(d['Class']),
                     tag_based=d['TagBased']=='True')
                    
    
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    score = Column(Integer)
    text = Column(String())
    creation_date = Column(DateTime)
    user_id = Column(Integer)
    
    @classmethod
    def parse_line(cls, line):
        x = line.strip()
        if x[1:4] != 'row':
            return
        d = BeautifulSoup(x, 'xml').find('row').attrs
        
        for label in ('Id', 'PostId', 'Score', 'Text', 'CreationDate', 'UserId'):
            if label not in d:
                d[label] = None
                
        return Comment(id=int_conv(d['Id']),
                       post_id=int_conv(d['PostId']),
                       score=int_conv(d['Score']),
                       text=d['Text'],
                       creation_date=string_to_dt(d['CreationDate']),
                       user_id=int_conv(d['UserId']))
    
class PostRecord(Base):
    __tablename__ = 'post_record'
    id = Column(Integer, primary_key=True)
    post_history_type_id = Column(Integer)
    post_id = Column(Integer)
    revision_guid = Column(String(36))
    creation_date = Column(DateTime)
    user_id = Column(Integer)
    text = Column(String())
    
    @classmethod
    def parse_line(cls, line):
        x = line.strip()
        if x[1:4] != 'row':
            return
        d = BeautifulSoup(x, 'xml').find('row').attrs
        
        for label in ('Id', 'PostHistoryTypeId', 'PostId', 'RevisionGUID', 'CreationDate', 'UserId', 'Text'):
            if label not in d:
                d[label] = None
                
        return PostRecord(id=int_conv(d['Id']),
                          post_history_type_id=int_conv(d['PostHistoryTypeId']),
                          post_id=int_conv(d['PostId']),
                          revision_guid=d['RevisionGUID'],
                          creation_date=string_to_dt(d['CreationDate']),
                          user_id=int_conv(d['UserId']),
                          text=d['Text'])
        
class PostLink(Base):
    __tablename__ = 'post_link'
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime)
    post_id = Column(Integer)
    related_post_id = Column(Integer)
    link_type_id = Column(Integer)
    
    @classmethod
    def parse_line(cls, line):
        x = line.strip()
        if x[1:4] != 'row':
            return
        d = BeautifulSoup(x, 'xml').find('row').attrs
        
        for label in ('Id', 'CreationDate', 'PostId', 'RelatedPostId', 'LinkTypeId'):
            if label not in d:
                d[label] = None
                
        return PostLink(id=int(d['Id']),
                        creation_date=string_to_dt(d['CreationDate']),
                        post_id=int_conv(d['PostId']),
                        related_post_id=int_conv(d['RelatedPostId']),
                        link_type_id=int_conv(d['LinkTypeId']))
        
class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(250))
    count = Column(Integer)
    excerpt_post_id= Column(Integer)
    wiki_post_id=Column(Integer)
    
    @classmethod
    def parse_line(cls, line):
        x = line.strip()
        if x[1:4] != 'row':
            return
        d = BeautifulSoup(x, 'xml').find('row').attrs
        
        for label in ('Id', 'TagName', 'Count', 'ExcerptPostId', 'WikiPostId'):
            if label not in d:
                d[label] = None
                
        return Tag(id=int_conv(d['Id']),
                   tag_name=d['TagName'],
                   count=int_conv(d['Count']),
                   excerpt_post_id=int_conv(d['ExcerptPostId']),
                   wiki_post_id=int_conv(d['WikiPostId']))
        

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    reputation = Column(Integer)
    creation_date = Column(DateTime)
    display_name = Column(String(250))
    last_access_date = Column(DateTime)
    website_url = Column(String())
    location = Column(String())
    about_me = Column(String())
    views = Column(Integer)
    up_votes = Column(Integer)
    down_votes = Column(Integer)
    account_id = Column(Integer)
    
    @classmethod
    def parse_line(cls, line):
        x = line.strip()
        if x[1:4] != 'row':
            return
        d = BeautifulSoup(x, 'xml').find('row').attrs
        
        for label in ('Id',
                      'Reputation',
                      'CreationDate',
                      'DisplayName',
                      'LastAccessDate',
                      'WebsiteUrl',
                      'Location',
                      'AboutMe',
                      'Views',
                      'UpVotes',
                      'DownVotes',
                      'AccountId'):
            if label not in d:
                d[label] = None
        
        return User(id=int_conv(d['Id']),
                    reputation=int_conv(d['Reputation']),
                    creation_date=string_to_dt(d['CreationDate']),
                    display_name=d['DisplayName'],
                    last_access_date=string_to_dt(d['LastAccessDate']),
                    website_url=d['WebsiteUrl'],
                    location=d['Location'],
                    about_me=d['AboutMe'],
                    views=int_conv(d['Views']),
                    up_votes=int_conv(d['UpVotes']),
                    down_votes=int_conv(d['DownVotes']),
                    account_id=int_conv(d['AccountId']))
        
        
class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    vote_type_id = Column(Integer)
    creation_date = Column(DateTime)
    
    @classmethod
    def parse_line(cls, line):
        x = line.strip()
        if x[1:4] != 'row':
            return
        d = BeautifulSoup(x, 'xml').find('row').attrs
        
        for label in ('Id', 'PostId', 'VoteTypeId', 'CreationDate'):
            if label not in d:
                d[label] = None
                
        return Vote(id=int_conv(d['Id']),
                    post_id=int_conv(d['PostId']),
                    vote_type_id=int_conv(d['VoteTypeId']),
                    creation_date=string_to_dt(d['CreationDate']))
        

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    post_type_id = Column(String())
    parent_id = Column(Integer)
    accepted_answer_id = Column(Integer)
    creation_date = Column(DateTime)
    score = Column(Integer)
    view_count = Column(Integer)
    body = Column(String())
    owner_user_id = Column(Integer)
    last_editor_user_id = Column(Integer)
    last_editor_display_name = Column(String())
    last_edit_date = Column(DateTime)
    last_activity_date = Column(DateTime)
    community_owned_date = Column(DateTime)
    closed_date = Column(DateTime)
    title = Column(String())
    tags = Column(String())
    answer_count = Column(Integer)
    comment_count = Column(Integer)
    favorite_count = Column(Integer)
    
    @classmethod
    def parse_line(cls, line):
        x = line.strip()
        if x[1:4] != 'row':
            return
        d = BeautifulSoup(x, 'xml').find('row').attrs
        
        for label in ('Id',
                      'PostTypeId',
                      'ParentId',
                      'AcceptedAnswerId',
                      'CreationDate',
                      'Score',
                      'ViewCount',
                      'Body',
                      'OwnerUserId',
                      'LastEditorUserId',
                      'LastEditorDisplayName',
                      'LastEditDate',
                      'LastActivityDate',
                      'CommunityOwnedDate',
                      'ClosedDate',
                      'Title',
                      'Tags',
                      'AnswerCount',
                      'CommentCount',
                      'FavoriteCount'):
            if label not in d:
                d[label] = None
                
        return Post(id=int_conv(d['Id']),
                    post_type_id=int_conv(d['PostTypeId']),
                    parent_id=int_conv(d['ParentId']),
                    accepted_answer_id=int_conv(d['AcceptedAnswerId']),
                    creation_date=string_to_dt(d['CreationDate']),
                    score=int_conv(d['Score']),
                    view_count=int_conv(d['ViewCount']),
                    body=d['Body'],
                    owner_user_id=int_conv(d['OwnerUserId']),
                    last_editor_user_id=int_conv(d['LastEditorUserId']),
                    last_editor_display_name=d['LastEditorDisplayName'],
                    last_edit_date=string_to_dt(d['LastEditDate']),
                    last_activity_date=string_to_dt(d['LastActivityDate']),
                    community_owned_date=string_to_dt(d['CommunityOwnedDate']),
                    closed_date=string_to_dt(d['ClosedDate']),
                    title=d['Title'],
                    tags=d['Tags'],
                    answer_count=int_conv(d['AnswerCount']),
                    comment_count=int_conv(d['CommentCount']),
                    favorite_count=int_conv(d['FavoriteCount']))