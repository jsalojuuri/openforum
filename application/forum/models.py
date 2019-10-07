from application import db
from application.models import Base
from sqlalchemy.sql import text

class Topic(Base):

    title = db.Column(db.String(144), nullable=False)
    bodytxt = db.Column(db.String(1444), nullable=False)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    topicaccounts = db.relationship("Topicaccount", cascade="delete", backref='topic', lazy=True)
    topic_comments = db.relationship("Comment", cascade="delete", backref='topic', lazy=True)
    
    def __init__(self, title, bodytxt):
        self.title = title
        self.bodytxt = bodytxt
    
    @staticmethod
    def find_topics_by_forum(forum_id):
        stmt = text("SELECT Topic.id, Topic.title, Topic.bodytxt, Topic.date_modified, Topic.forum_id, Account.name, Account.id, COUNT(DISTINCT Comment.id) FROM Topic"
                    " LEFT JOIN Topicaccount ON Topicaccount.topic_id = Topic.id"
                    " LEFT JOIN Account ON Account.id = Topicaccount.account_id"
                    " LEFT JOIN Comment ON Topic.id = Comment.topic_id"
                    " WHERE (Topic.forum_id = :forum_id AND Topicaccount.creator = :creator_true)"
                    " GROUP BY Topic.id, Account.id").params(forum_id=forum_id, creator_true=1)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"id":row[0], "title":row[1], "bodytxt":row[2], "date_modified":row[3], "forum_id":row[4], "account_name":row[5], "account_id":row[6], "comment_count":row[7]})

        return response

    @staticmethod
    def find_topic_data(topic_id):
        stmt = text("SELECT Topic.title, Topic.bodytxt, Topic.date_modified, Account.name, Topic.id, Topic.forum_id FROM Topic"
                    " LEFT JOIN Topicaccount ON Topic.id = Topicaccount.topic_id"
                    " LEFT JOIN Account ON Topicaccount.account_id = Account.id"
                    " WHERE (Topic.id = :topic_id AND Topicaccount.creator = :creator_true)"
                    " GROUP BY Topic.id, Account.name").params(topic_id=topic_id, creator_true=1)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"title":row[0], "bodytxt":row[1], "date_modified":row[2], "account_name":row[3], "id":row[4], "forum_id":row[5]})

        return response

    @staticmethod
    def find_user_topics(account_id):
        stmt = text("SELECT Topic.id, Topic.title, Topic.bodytxt, Topic.date_modified, Topic.forum_id FROM Topic"
                    " LEFT JOIN Topicaccount ON Topic.id = Topicaccount.topic_id"
                    " WHERE (Topicaccount.account_id = :account_id AND Topicaccount.creator = :creator_true)"
                    " GROUP BY Topic.id"
                    " ORDER BY Topic.id").params(account_id=account_id, creator_true=1)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"id":row[0], "title":row[1], "bodytxt":row[2], "date_modified":row[3], "forum_id":row[4]})

        return response

    @staticmethod
    def find_user_topic_count(account_id):
        stmt = text("SELECT COUNT(DISTINCT Topic.id) FROM Topic"
                    " LEFT JOIN Topicaccount ON Topic.id = Topicaccount.topic_id"
                    " WHERE Topicaccount.account_id = :account_id AND Topicaccount.creator = :creator_true").params(account_id=account_id, creator_true=1)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"topic_count":row[0]})

        return response

    @staticmethod
    def find_user_comment_count(account_id):
        stmt = text("SELECT COUNT(Comment.id) FROM Comment"
                    " WHERE Comment.account_id = :account_id").params(account_id=account_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"comment_count":row[0]})

        return response
    

class Topicaccount(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    creator = db.Column(db.Boolean, nullable=False)
    viewer = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

    def __init__(self, creator, viewer):
        self.creator = creator
        self.viewer = viewer
    
    @staticmethod
    def find_topic_viewer_count(topic_id):
        stmt = text("SELECT COUNT(DISTINCT Topicaccount.account_id), COUNT(Topicaccount.account_id) FROM Topicaccount"
                    " WHERE (Topicaccount.topic_id = :topic_id AND Topicaccount.viewer = :topic_viewer_true)"
                    ).params(topic_id=topic_id, topic_viewer_true=1)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"viewer_count":row[0], "view_count":row[1]})

        return response 

class Comment(Base):

    bodytxt = db.Column(db.String(1444), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

    def __init__(self, bodytxt):
        self.bodytxt = bodytxt     

    @staticmethod
    def find_comments_by_forum(forum_id):
        stmt = text("SELECT Account.name, Account.id, Comment.id, Comment.bodytxt, Comment.date_modified, Comment.topic_id FROM Comment"
                    " LEFT Join Topic ON Topic.id = Comment.topic_id"
                    " LEFT JOIN Account ON Account.id = Comment.account_id"
                    " WHERE (Topic.forum_id = :forum_id)"
                    " GROUP BY Topic.id").params(forum_id=forum_id)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"account_name":row[0], "account_id":row[1], "comment_id":row[2], "comment_bodytxt":row[3], "comment_date_modified":row[4], "comment_topic_id":row[5]})

        return response     

    @staticmethod
    def find_comments_by_topic(topic_id):
        stmt = text("SELECT Account.name, Comment.bodytxt, Comment.date_modified FROM Comment"
                    " LEFT JOIN Account ON Comment.account_id = Account.id"
                    " WHERE (Comment.topic_id = :topic_id)"
                    ).params(topic_id=topic_id)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"account_name":row[0], "comment_bodytxt":row[1], "comment_date_modified":row[2]})

        return response     

    @staticmethod
    def find_user_comments(account_id):
        stmt = text("SELECT Topic.forum_id, Topic.id, Topic.title, Comment.bodytxt, Comment.date_modified, Comment.id FROM Comment"
                    " LEFT JOIN Topic ON Comment.topic_id = Topic.id"
                    " WHERE (Comment.account_id = :account_id)"
                    " GROUP BY Topic.id, Comment.id"
                    " ORDER BY Topic.id").params(account_id=account_id)
        res = db.engine.execute(stmt)
  
        response = []
        for row in res:
            response.append({"forum_id":row[0], "topic_id":row[1], "topic_title":row[2], "comment_bodytxt":row[3], "comment_date_modified":row[4], "comment_id":row[5]})

        return response