from pathlib import Path
import sqlite3 as sqlite
import flet as ft
from datetime import datetime
from domain_model.user import User
from domain_model.chat import Chat
from typing import List
import json

class Database:
    def __init__(self):
        self.db = None

    def connect_to_db(self):
        try:
            db_path = Path(__file__).parent.parent.joinpath("predacons.db")
           
            self.db_path = db_path
            self.db = sqlite.connect(db_path)
            c = self.db.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
								  name VARCHAR(100) NOT NULL, 
								  createddate DATETIME NOT NULL, 
                                  lastupdated DATETIME NOT NULL, 
								  vertexapikey VARCHAR(255),
								  openaiapikey VARCHAR(255),
								  azureendpoint VARCHAR(255),
								  azureapikey VARCHAR(255),
								  azureapiversion VARCHAR(255), 
								  azuredeploymentname VARCHAR(255),
                                  maxhistory INT,
								  metadata TEXT)""")
            
            c.execute(
                """CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  title VARCHAR(255) NOT NULL UNIQUE,
                                  type VARCHAR(255),
                                  createddate DATETIME NOT NULL,
                                  lastupdated DATETIME NOT NULL, 
                                  vectordb VARCHAR(255),
                                  websearch BOOLEAN,
                                  sytemprompt TEXT,
                                  chat TEXT,
                                  metadata TEXT)""")
            
            print("Database connected and table ensured.")
            
        except sqlite.DatabaseError as e:
            print("Error: Database not found")
            print(e)
    
    # crud op on user
    def return_db_path(self):
        return self.db_path
    def read_user_db(self):
        """ Read user data from database """
        c = self.db.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        
        users = []
        for row in rows:
            user = User(
                id=row[0], 
                name=row[1], 
                createddate=row[2], 
                lastupdated=row[3], 
                vertexapikey=row[4], 
                openaiapikey=row[5], 
                azureendpoint=row[6], 
                azureapikey=row[7], 
                azureapiversion=row[8], 
                azuredeploymentname=row[9], 
                maxhistory=row[10], 
                metadata=row[11]
            )
            users.append(user)
        
        return users
    
    def create_user(self, user):
        """ Create a new user """
        c = self.db.cursor()
        c.execute(
            """INSERT INTO users (name, createddate, lastupdated, vertexapikey, openaiapikey, azureendpoint, azureapikey, azureapiversion, azuredeploymentname, maxhistory, metadata) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user.name, datetime.now(), datetime.now(), user.vertexapikey, user.openaiapikey, 
                user.azureendpoint, user.azureapikey, user.azureapiversion, user.azuredeploymentname, 
                user.maxhistory, user.metadata
            )
        )
        self.db.commit()
        return c.lastrowid
    
    def update_user(self, user):
        """ Update an existing user """
        c = self.db.cursor()
        c.execute(
            """UPDATE users SET name = ?, vertexapikey = ?, openaiapikey = ?, azureendpoint = ?, azureapikey = ?, azureapiversion = ?, 
            azuredeploymentname = ?, maxhistory = ?, metadata = ?, lastupdated = ? WHERE id = ?""",
            (
                user.name, user.vertexapikey, user.openaiapikey, user.azureendpoint, user.azureapikey, user.azureapiversion, 
                user.azuredeploymentname, user.maxhistory, user.metadata, datetime.now(), user.id
            )
        )
        self.db.commit()
    
    # crud op on chat
    def read_chat_db(self, filters=None, sort_by=None, limit=None) -> List[Chat]:
        """
        Read chat data from database with optional filters, sorting, and limit.
        
        :param filters: Dictionary of column-value pairs to filter the results.
        :param sort_by: Column name to sort the results by.
        :param limit: Maximum number of results to return.
        :return: List of Chat objects matching the query.
        """
        query = "SELECT * FROM chats"
        params = []

        # Apply filters
        if filters:
            filter_clauses = []
            for column, value in filters.items():
                filter_clauses.append(f"{column} = ?")
                params.append(value)
            query += " WHERE " + " AND ".join(filter_clauses)

        # Apply sorting
        if sort_by:
            query += f" ORDER BY {sort_by}"

        # Apply limit
        if limit:
            query += f" LIMIT {limit}"

        c = self.db.cursor()
        c.execute(query, params)
        rows = c.fetchall()

        chats = []
        for row in rows:
            chat = Chat(
                id=row[0],
                title=row[1],
                type=row[2],
                createddate=row[3],
                lastupdated=row[4],
                vectordb=row[5],
                websearch=row[6],
                sytemprompt=row[7],
                chat=row[5],
                metadata=row[6]
            )
            chats.append(chat)

        return chats
        
    def get_chat_by_id(self, chat_id) -> Chat:
        """ Get a chat by its ID """
        c = self.db.cursor()
        c.execute("SELECT * FROM chats WHERE id = ?", (chat_id,))
        row = c.fetchone()
        if row:
            chat = Chat(
                id=row[0],
                title=row[1],
                type=row[2],
                createddate=row[3],
                lastupdated=row[4],
                vectordb=row[5],
                websearch=row[6],
                sytemprompt=row[7],
                chat=row[5],
                metadata=row[6]
            )
            return chat
        return None
    def insert_chat(self, chat: Chat):
        """ Insert a new chat into the chats table """
        c = self.db.cursor()
        c.execute(
            """INSERT INTO chats (title, type, createddate, lastupdated, vectordb, websearch, sytemprompt, chat, metadata) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                chat.title, chat.type, datetime.now(), datetime.now(), chat.vectordb, chat.websearch, chat.sytemprompt, chat.chat, chat.metadata
            )
        )
        self.db.commit()
        return c.lastrowid
    def insert_multiple_chats(self, chats: List[Chat]):
        """
        Insert multiple chats into the chats table.
        
        :param chats: List of Chat objects.
        """
        try:
            c = self.db.cursor()
            chat_tuples = [
                (
                    chat.title, chat.type, datetime.now, datetime.now, chat.vectordb, chat.websearch, chat.sytemprompt, chat.chat, chat.metadata
                )
                for chat in chats
            ]
            c.executemany(
                """INSERT INTO chats (title, type, createddate, lastupdated, vectordb, websearch, sytemprompt, chat, metadata) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                chat_tuples
            )
            self.db.commit()
            print("Multiple chats inserted successfully.")
        except sqlite.DatabaseError as e:
            print("Error: Failed to insert multiple chats")
            print(e)
        
    def update_chat(self, chat: Chat):
        """ Update an existing chat """
        c = self.db.cursor()
        c.execute(
            """UPDATE chats SET title = ?, type = ?, createddate = ?, lastupdated = ?, vectordb = ?, websearch = ?, sytemprompt = ?, chat = ?, metadata = ? WHERE id = ?""",
            (
                chat.title, chat.type, chat.createddate, chat.lastupdated, chat.vectordb, chat.websearch, chat.sytemprompt, chat.chat, chat.metadata, chat.id
            )
        )
        self.db.commit()

    def delete_chat(self, chat_id):
        """ Delete a chat by its ID """
        c = self.db.cursor()
        c.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
        self.db.commit()

    def close_db(self):
        """ Close the database connection """
        if self.db:
            self.db.close()
            print("Database connection closed.")

