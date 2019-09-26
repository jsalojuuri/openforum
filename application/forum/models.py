from application import db
from application.models import Base

from sqlalchemy.sql import text

class Topic(Base):

    title = db.Column(db.String(144), nullable=False)
    bodytxt = db.Column(db.String(14444), nullable=False)

    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    topicaccounts = db.relationship("Topicaccount", cascade="delete", backref='topic', lazy=True)

    def __init__(self, title, bodytxt):
        self.title = title
        self.bodytxt = bodytxt
    
    @staticmethod
    def find_topics_by_forum(forum_id):
        stmt = text("SELECT Topic.id, Topic.title, Topic.bodytxt, Topic.date_modified, Topic.forum_id, Account.name, Account.id FROM Topic"
                    " LEFT JOIN Topicaccount ON Topicaccount.topic_id = Topic.id"
                    " LEFT JOIN Account ON Account.id = Topicaccount.account_id"
                    " WHERE (Topic.forum_id = :forum_id)"
                    " GROUP BY Topic.id, Account.id").params(forum_id=forum_id)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"id":row[0], "title":row[1], "bodytxt":row[2], "date_modified":row[3], "forum_id":row[4], "account_name":row[5], "account_id":row[6]})

        return response


    @staticmethod
    def find_user_topics(account_id):
        stmt = text("SELECT Topic.id, Topic.title, Topic.bodytxt, Topic.date_modified, Topic.forum_id, Account.name, Account.id FROM Topic"
                    " LEFT JOIN Topicaccount ON Topicaccount.topic_id = Topic.id"
                    " LEFT JOIN Account ON Account.id = Topicaccount.account_id"
                    " WHERE (Account.id = :account_id)"
                    " GROUP BY Account.id, Topicaccount.topic_id, Topic.id").params(account_id=account_id)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"id":row[0], "title":row[1], "bodytxt":row[2], "date_modified":row[3], "forum_id":row[4], "account_name":row[5], "account_id":row[6]})

        return response

    @staticmethod
    def find_user_statistics(account_id):
        stmt = text("SELECT COUNT(DISTINCT Topic.id), COUNT(Topicaccount.creator), COUNT(Topicaccount.account_id) FROM Topic"
                    " LEFT JOIN Topicaccount ON Topicaccount.topic_id = topic.id"
                    " WHERE (Topicaccount.account_id = :account_id)").params(account_id=account_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"topic_count":row[0], "creator":row[0], "account_id":row[0]})

        return response
    


class Topicaccount(Base):

    creator = db.Column(db.Boolean, nullable=False)
    viewer = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

    def __init__(self, creator, viewer):
        self.creator = creator
        self.viewer = viewer
            
