from datetime import datetime

class Chat:
    def __init__(self, id: int, title: str, createddate: datetime, lastupdated: datetime, 
                 type: str = None, chat: str = None, metadata: str = None):
        self.id = id
        self.title = title
        self.type = type
        self.createddate = createddate
        self.lastupdated = lastupdated
        self.chat = chat
        self.metadata = metadata

    def __repr__(self):
        return f"Chat(id={self.id}, title='{self.title}', type='{self.type}', createddate='{self.createddate}', lastupdated='{self.lastupdated}', chat='{self.chat}', metadata='{self.metadata}')"