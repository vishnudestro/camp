import json
import logging
from pprint import pprint

from bson.objectid import ObjectId
from pymongo import errors

from dynaconf import settings
from camp.controller import search_property, update_property

from camp.controller.mongo_collections import db, User, Company, Team, Project, Todo, Task, Comment, Chat_room, Message

logger = logging.getLogger(__name__)

#create team or project
def create_team_or_project(collection_name, create_list, company_id, user_id):
    """The function is to create a new team or project. 
    
    Parameters
    ----------
    collection_name : String
        name of the collection("team or project") that need to be created
    create_list : list
        list of team or project name wants to create
    company_id : ObjectId
        Id of the company
    user_id : ObjectId
        Id of the user
    
    Returns
    -------
    json, boolean
        return json data and true status about the process
    """
    response = {}
    member_list = collection_name+"_list"

    for name in create_list:
        #TODO: Fix duplicate issue team project creation issue
        
        #Check if the team or project  is already exist
        #If a team or project exist
        if db[collection_name].count_documents({"name":name, "company_id":company_id}) > 0: 
            #Check if the user was already exist in the team or project
            #If exist
            if db[collection_name].count_documents({"name":name, "company_id":company_id, "people_list":{"$in":[str(user_id)]}}) > 0:
                logger.warning(f'The {collection_name} {name} and the user {user_id} were already exist')
                return response, False
            
            #If doesn't exist
            else:
                db[collection_name].update({"name":name, "company_id":company_id},{"$push":{'people_list': str(user_id)}})
                update_status = update_property.update_company_data(collection_name, member_list, name, company_id, user_id)
                logger.info(f'The {collection_name} {name} was already exist and updated with the new user id: {user_id}')
        
        #If a team or project doesn't exist
        else:  
            #Insert a new team or project          
            db[collection_name].insert({"name":name, "company_id":company_id, "people_list":[str(user_id)], "delete_status": False})
            update_status = update_property.update_company_data(collection_name, member_list, name, company_id, user_id)
            logger.info(f'The {collection_name} {name} is created')
    
    #Form a output json
    create_list_data = db[collection_name].find({"name":create_list[0], "company_id":company_id, "people_list":{"$in":[str(user_id)]}})
    for data in create_list_data:
        response = {
            "team_id" : str(ObjectId(data['_id'])),
            "name": data['name'],
            "url" : "http://localhost:2000/todo/"+ str(ObjectId(data['_id'])),
            "people_list" : data['people_list']
        }
    
    return response, True 

#create todo
def create_todo(task_data = None, todo_id = None):  
    """The function is to create a new todo.
    
    Parameters
    ----------
    task_data : json, optional
        contain title, reference id, and a description by default None
    todo_id : ObjectId, optional
        Id of the todo, by default None
    
    Returns
    -------
    json, boolean
        return the create todo data as output and status (True or False)
    """
    
    #Check if the todo is already exist
    output, status = search_property.find_todo(task_data['title'], task_data['ref_id'], task_data['description'])
    collection_name = ["company", "team", "project"]

    #If doesn't exist
    if status == False:        
        for name in collection_name:
            if db[name].count({"_id":ObjectId(task_data['ref_id'])}) > 0:  
                #Insert a new todo          
                Todo.insert({
                    "name":task_data['title'], 
                    "ref_id":task_data['ref_id'], 
                    "description":task_data['description'], 
                    "task_list":[], 
                    "comment_list":[],
                    "delete_status": False
                })
                
                logger.info(f'The todo {task_data["title"]} is created')
                output, status = search_property.find_todo(task_data['title'], task_data['ref_id'], task_data['description'])
                
                #Update todo id in the team or the project's todo_list
                db[name].update({"_id":ObjectId(task_data['ref_id'])},{"$push":{"todo_list":str(output['data'][0]['_id'])}})
                return output['data'][0], status
    #If exist
    else:
        logger.warning(f'The todo {task_data["title"]} was already exist')
        return output, status

#create task
def create_task(todo_id = None, task_list = None):
    """The function is to create a new task
    
    Parameters
    ----------
    todo_id : OnjectId, optional
        Id of the todo, by default None
    task_list : json, optional
        Contain the task_id,todo_id,description about the task,person they assigned to and notify to and due date by default None
    
    Returns
    -------
    json
        contain the details about todo that was created
    """

    #Insert new Todo list
    task_id = ObjectId()
    Task.insert({
            "_id":task_id, 
            "todo_ref_id": todo_id,
            "description": task_list['description'],
            "assigned_to": task_list['assigned_to'],
            "notify_to": task_list['notify_to'],
            "due": task_list['due'],
            "comment_list":[],
            "delete_status": False
        })
    logger.info(f'The task {task_id} is created')
    
    #Update the Task Id in Todo collection
    Todo.update({"_id":ObjectId(todo_id)},{"$push":{"task_list":str(task_id)}})

    #Find Todo & Task details
    todo_details = search_property.find_todo_list(todo_id)
    response = {
        "description": todo_details['description'],
        "name":todo_details['name'],
        "todo_id":todo_details['todo_id']
    }
    
    #Get the task details if the task id match with any one of the task list id in todo_details
    for task in todo_details['task_details']:
        if str(task_id) == task['task_id']:
            response['task_details'] = task
    
    return response


#create comment
def create_comment(input_data):
    """The function is to create a new comments
    
    Parameters
    ----------
    input_data : json
        contains details about created at, created by, comments, and reference id the comment belongs to.
    
    Returns
    -------
    json, boolean
        return a json data and status response of (True or False) 
    """

    response = {}
    
    #Insert a new comment
    comment_id = ObjectId()
    Comment.insert(
        {
            "_id": comment_id,
            "created_at": input_data['created_at'],
            "created_by":input_data['created_by'],
            "comment": input_data['comment'],
            "ref_id":input_data['ref_id']
        })
    logger.info(f'The comment {comment_id} is created')

    #Check the where to update the comment whether in todo or the task
    try:
        if Todo.count({"_id":ObjectId(input_data['ref_id'])}) > 0:
            Todo.update({"_id":ObjectId(input_data['ref_id'])},{"$push":{"comment_list":str(comment_id)}})
        else:
            Task.update({"_id":ObjectId(input_data['ref_id'])},{"$push":{"comment_list":str(comment_id)}})
    except Exception as e:
        logger.error(f'The reference id {input_data["ref_id"]} does not exist')
        return response, False

    #Check the comment data where inserted
    #If inserted
    if Comment.count({"_id": comment_id}) > 0:
        data = search_property.find_user([input_data['created_by']])
        response = {
                "_id": str(comment_id),
                "created_at": input_data['created_at'],
                "comment": str(input_data['comment']),
                "ref_id":str(input_data['ref_id']),
            }
        response["created_by"] = data['user_data'][0]['person_name']
        response["job_title"] = data['user_data'][0]['job_title']

        return response, True
    #If not
    else:
        return response, False


#create chatroom
def create_chatroom(input_data):
    """The function is to create a new chatroom
    
    Parameters
    ----------
    input_data : json
        contains the data of company id and memeber who are all in that chatroom
    
    Returns
    -------
    json, boolean
        Returns the json and true status
    """
    
    #Check the chatroom was already exist
    chatroom_data = Chat_room.find({"company_id":input_data['company_id'], "members":input_data['members']})
    
    #If exist
    if chatroom_data.count() > 0:
        for data in chatroom_data:
            response = {
                "chatroom_id":str(ObjectId(data['_id'])),
                "company_id": str(data['company_id']),
                "url": "http://localhost:2000/"+ input_data['company_id'] + "/chat/" + str(ObjectId(data['_id']))
            }
        logger.warning(f'The chatroom {data["_id"]} was already exist')
        return response, True
    
    #If doesn't exist
    else:
        #Create a new chatroom
        chatroom_id = ObjectId()
        Chat_room.insert({
            "_id":chatroom_id,
            "company_id": input_data['company_id'],
            "members":input_data['members'],
            "message_list":[]
        })
        logger.info(f'Chatroom {chatroom_id} is created')
        response = {
            "chatroom_id":str(chatroom_id),
            "url": "http://localhost:2000/"+ input_data['company_id'] + "/chat/" + str(chatroom_id)
        }
        return response, True

#Create message
def create_message(input_data):
    """The function is to create a new message
    
    Parameters
    ----------
    input_data : json
        contains the data about message id, created at, created by, message and the chatroom id the message belongs
    
    Returns
    -------
    String, boolean
        returns the message id and the true status
    """
    
    message_data = {}
    message_id = ObjectId()

    #Search for the user information who created the message
    user = search_property.find_user([input_data['created_by']])
    
    #Form a message data
    message_data["_id"] = message_id
    message_data["chatroom_id"] = input_data['chatroom_id']
    message_data["created_at"] = input_data['created_at']
    message_data["message"] = input_data['message']

    message_data["created_by"] = {
        "user_id":user['user_data'][0]['_id'],
        "person_name":user['user_data'][0]['person_name']
    }
    
    #Insert a new message
    Message.insert(message_data)
    logger.info(f'The message {message_id} is created')
    
    #Update the message id in the chatroom's message list
    Chat_room.update({
        "_id":ObjectId(input_data['chatroom_id'])
    },{
        "$push":{"message_list":str(message_id)}
    })

    return str(message_id), True