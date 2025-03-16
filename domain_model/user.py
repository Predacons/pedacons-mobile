from datetime import datetime

class User:
    def __init__(self, id: int=None, name: str=None, createddate: datetime=None, lastupdated: datetime=None, 
                 vertexapikey: str = None, openaiapikey: str = None, azureendpoint: str = None, 
                 azureapikey: str = None, azureapiversion: str = None, azuredeploymentname: str = None, 
                 maxhistory: int = None, metadata: str = None):
        self.id = id
        self.name = name
        self.createddate = createddate
        self.lastupdated = lastupdated
        self.vertexapikey = vertexapikey
        self.openaiapikey = openaiapikey
        self.azureendpoint = azureendpoint
        self.azureapikey = azureapikey
        self.azureapiversion = azureapiversion
        self.azuredeploymentname = azuredeploymentname
        self.maxhistory = maxhistory
        self.metadata = metadata

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', createddate='{self.createddate}', lastupdated='{self.lastupdated}', vertexapikey='{self.vertexapikey}', openaiapikey='{self.openaiapikey}', azureendpoint='{self.azureendpoint}', azureapikey='{self.azureapikey}', azureapiversion='{self.azureapiversion}', azuredeploymentname='{self.azuredeploymentname}', maxhistory={self.maxhistory}, metadata='{self.metadata}')"