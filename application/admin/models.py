from application import db
from application.models import Base

from sqlalchemy.sql import text

class Forum(Base):

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    topics = db.relationship("Topic", backref='forum', lazy=True)

    def __init__(self, name):
        self.name = name
    

    @staticmethod
    def forum_statistics():
        stmt = text("SELECT Forum.id, Forum.name, Forum.description, Forum.date_modified, COUNT(DISTINCT Forum.id), COUNT(DISTINCT Topic.id), COUNT(DISTINCT Topicaccount.account_id) FROM Forum"
                    " LEFT JOIN Topic ON Topic.forum_id = Forum.id"
                    " LEFT JOIN Topicaccount ON Topicaccount.topic_id = Topic.id"
                    " GROUP BY Forum.id")
                      
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            
            response.append({"id":row[0], "name":row[1], "description":row[2], "date_modified":row[3], "forum_count":row[4], "topic_count":row[5], "account_count":row[6]})

        return response


    @staticmethod
    def forum_statistics_by_forum():
        stmt = text("SELECT Forum.id, Forum.name, Forum.description, Forum.date_modified, COUNT(DISTINCT Topic.id), COUNT(DISTINCT Topicaccount.account_id) FROM Forum"
                    " LEFT JOIN Topic ON Topic.forum_id = Forum.id"
                    " LEFT JOIN Topicaccount ON Topicaccount.topic_id = Topic.id"
                    " GROUP BY Forum.id ")        
                
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            
            response.append({"id":row[0], "name":row[1], "description":row[2], "date_modified":row[3], "topic_count":row[4], "account_count":row[5]})

        return response