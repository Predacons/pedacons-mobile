from datetime import datetime
import random

class Chat:
    def __init__(self, id: int = None, title: str = 'New Chat', createddate: datetime = None, lastupdated: datetime =None, 
                 type: str = None, chat: str = None, metadata: str = None, 
                 vectordb: str = None, websearch: bool = False, sytemprompt: str = None):
        self.id = id
        self.title = title + str(random.randint(1, 1000))
        self.type = type
        self.createddate = createddate
        self.lastupdated = lastupdated
        self.chat = chat
        self.metadata = metadata
        self.vectordb = vectordb
        self.websearch = websearch
        self.sytemprompt = sytemprompt

    def __repr__(self):
        return (f"Chat(id={self.id}, title='{self.title}', type='{self.type}', createddate='{self.createddate}', "
                f"lastupdated='{self.lastupdated}', chat='{self.chat}', metadata='{self.metadata}', "
                f"vectordb='{self.vectordb}', websearch={self.websearch}, sytemprompt='{self.sytemprompt}')")