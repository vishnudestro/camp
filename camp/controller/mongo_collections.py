from pymongo import MongoClient, errors

from dynaconf import settings

#Mongo Conncection

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client.camp

#Collections
Team = db.team 
Project = db.project
Company = db.company
User = db.user_details
Invites = db.invites
Todo = db.todo
Task = db.task
Comment = db.comment
Chat_room = db.chatroom
Message = db.message