from flask_mongoengine import MongoEngine, Document
from flask_login import UserMixin

from camp import login_manager, db

class User(UserMixin, db.Document):
    meta = {'collection': 'user_details'}
    email = db.StringField(max_length = 50)
    password = db.StringField()
    person_name = db.StringField(max_length = 50)
    company_id = db.StringField()
    job_title = db.StringField(default = "")

class Company(db.Document):
    meta = {'collection': 'company'}
    name = db.StringField(max_length = 50)
    people_list = db.ListField()
    team_list = db.ListField()
    project_list = db.ListField()
    todo_list = db.ListField()

class Invites(db.Document):
    meta = {'collection': 'invites'}
    co_worker_email = db.StringField(max_length = 50)
    co_worker_name = db.StringField(max_length = 50)
    company_id = db.StringField()
    invite_id = db.StringField()
    invite_status = db.BooleanField(default = False)

class Reset_invites(db.Document):
    meta = {'collection': 'reset_invites'}
    email = db.StringField(max_length = 50)
    company_id = db.StringField()
    reset_id = db.StringField()
    reset_status = db.BooleanField(default = False)

class Todo(db.Document):
    meta = {'collection': 'todo'}
    task_name = db.StringField()
    ref_id = db.StringField()
    description = db.StringField()
    task_list = db.ListField()
    comment_list = db.ListField()
    delete_status = db.BooleanField(default = False)

class Chatroom(db.Document):
    meta = {'collection': 'chatroom'}
    company_id = db.StringField()
    members = db.ListField()
    message_list = db.ListField()

class Message(db.Document):
    meta = {'collection': 'message'}
    chatroom_id = db.StringField()
    message = db.StringField()
    created_at = db.DateTimeField()
    created_by = db.DictField()

class Project(db.Document):
    meta = {'collection': 'project'}
    name = db.StringField()
    company_id = db.StringField()
    people_list = db.ListField()
    delete_status = db.BooleanField(default = False)
    todo_list = db.ListField()

class Team(db.Document):
    meta = {'collection': 'team'}
    name = db.StringField()
    company_id = db.StringField()
    people_list = db.ListField()
    delete_status = db.BooleanField(default = False)
    todo_list = db.ListField()

class Task(db.Document):
    meta = {'collection': 'task'}
    todo_ref_id = db.StringField()
    description = db.StringField()
    assigned_to = db.ListField()
    notify_to = db.ListField()
    due = db.DictField()
    delete_status = db.BooleanField(default = False)
    comment_list = db.ListField()

class Comment(db.Document):
    meta = {'collection': 'comment'}
    created_at = db.DateTimeField()
    created_by = db.StringField()
    comment = db.StringField()
    ref_id = db.StringField()


#User Loader
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.objects(pk = user_id).first()
    except Exception as e:
        return None
        print('load user in user_manager', e)