from sqlalchemy import Column, Integer, String
from blog.database.database import Base

class Post(Base):
    __tablename__ = 'posts'
    
    url = Column(String(50), primary_key=True)
    title = Column(String(50), unique=True)
    date = Column(String(20))
    summary = Column(String(360))
    content = Column(String)

    def __init__(self, url=None, title=None, date=None, summary=None, content=None):
        self.url = url
        self.title = title
        self.date = date
        self.summary = summary
        self.content = content

    def __repr__(self):
        return f'<Post {self.title!r}>'
