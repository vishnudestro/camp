import json
from pprint import pprint
import logging

from bson.objectid import ObjectId

from dynaconf import settings
from camp.controller.mongo_collections import db, User, Company, Team, Project, Todo, Task, Comment, Chat_room, Message

logger = logging.getLogger(__name__)


def dasboard_json(user_id, company_id):
    """ The function used to form a json data for the dashboard that contain the data of team, project and company.
    
    Parameters
    ----------
    user_id : ObjectId
        contain's id of the user
    company_id : ObjectId
        contain's the id of the company
    
    Returns
    -------
    json, boolean
        return json response and boolean status(true or false)
    """

    response = {}
    #Find the company data by its id.
    company_data = Company.find({"_id":ObjectId(company_id)})

    #If exist
    if company_data.count() > 0: 
        #Get the project list and team list data.
        for each in company_data:
            search_data = {"project_list":each['project_list'], "team_list":each['team_list']}

        #Get details of each team and project
        output = team_project(search_data, user_id)

        #Find the user details belongs to the company
        users = find_user(each["people_list"])

        #Form a response json
        response["hq"] = {
            "_id":company_id, 
            "name":each["name"],
            "url": "http://localhost:2000/todo/" + str(ObjectId(company_id)),
            "people_list":users['user_data']
            }
        
        response["team"] = output["team"]
        response["projects"] = output["projects"]
        
        logger.info(f'The company {company_id} and user {user_id}, dasboard properties were created')
        return response, True
    
    #If doesn't exist
    else:
        logger.warning(f'The company {company_id} does not exist')
        return response, False


def team_project(response, user_id):
    """Used to find the data of all the team and projects in a company.
    
    Parameters
    ----------
    response : 
        contains the data that need to search for team and project.
    user_id : Object Id
        Id of the user
    
    Returns
    -------
    json
        the output json contains the data about team and project.
    """
    output = {}
    output["team"] = []
    output["projects"] = []
    
    #Find the data of all the team in a company.
    for team_id in response["team_list"]:
        team_data = Team.find({"_id":ObjectId(team_id), "people_list":{"$in":[user_id]}, "delete_status": False})
        
        for team in team_data:
            users = find_user(team['people_list'])
            output["team"].append(
                {   
                    "_id":str(ObjectId(team['_id'])),
                    "name": team["name"],
                    "url" : "http://localhost:2000/todo/"+str(ObjectId(team['_id'])),
                    "people_list": users['user_data']
                })

    #Find the data of all the project in a company.
    for project_id in response["project_list"]:
        project_data = Project.find({"_id":ObjectId(project_id), "people_list":{"$in":[user_id]}, "delete_status": False})
        
        for project in project_data:
            users = find_user(project['people_list'])  
            output["projects"].append(
                {   
                    "_id":str(ObjectId(project['_id'])),
                    "name": project["name"],
                    "url" : "http://localhost:2000/todo/"+str(ObjectId(project['_id'])),
                    "people_list": users['user_data']
                })
    
    return output


def check_if_exists(company_id):
    """The function is to check the company is exist or not
    
    Parameters
    ----------
    company_id : ObjectId
        Id of the company
    
    Returns
    -------
    [type]
        [description]
    """
    #Check the company is exist or not by id.
    company_exists = Company.count_documents({"_id":ObjectId(company_id)})
    if company_exists > 0:
        logger.info(f'The company {company_id} is exist')
        return True
    else:
        logger.info(f'The company {company_id} does not exist')
        return False


def find_company_data(company_id):
    """[summary]
    
    Parameters
    ----------
    company_id : ObjectId
        contains the company id
    
    Returns
    -------
    json
        The json contains details about the company.
    """
    #Find company data using its id.
    response = {}
    company_data = Company.find({"_id":ObjectId(company_id)})
    if company_data.count() > 0:
        for data in company_data:
            people_list = find_user(data['people_list'])
            response = {
                "company_id": str(ObjectId(data['_id'])),
                "company_name": data['name'],
                "people_list": [user for user in people_list['user_data']],
            }
    else:
        logger.warning(f'The company id: {company_id} data were not found')
        return response
    
    logger.info(f'The company id: {company_id} data were found')
    return response


def find_user(people_list):
    """[summary]
    
    Parameters
    ----------
    people_list : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """
    user_list = {}
    user_list["user_data"] = []
    
    #Get a user list and get each user details
    for people_id in people_list:
        user_details = User.find({"_id":ObjectId(people_id)})
        for user_data in user_details:
            user_list["user_data"].append({
                "_id" : str(ObjectId(user_data['_id'])),
                "email" : user_data['email'],
                "job_title" : user_data['job_title'],
                "person_name" : user_data['person_name'],
                "company_id" : str(user_data['company_id']),
            })
    logger.info('User data created')
    return user_list


def find_team_project_company(collection_name = None, _id = None, user_id = None):
    """The function is to identify where the given id belongs to whether the team or project or the company according to that it has to
    
    Parameters
    ----------
    collection_name : string, optional
        Name of the collection where the data dhould be searched, by default None
    _id : ObjecId, optional
        This might belongs to the tea or project or the company, by default None
    user_id : ObjectID, optional
        Contains the user id, by default None
    
    Returns
    -------
    json
        Contain's the json information aabout the team or project or the company.
    """
    response = {}
    if collection_name == None:  
        collection_name = ["company", "team", "project"]
        for name in collection_name:
            data = db[name].find({"_id":ObjectId(_id)})
            if data.count() > 0:
                collection_name = name
                logger.info(f'The collection name is set to {collection_name}')
                break
    else:
        data = db[collection_name].find({"_id":ObjectId(_id), "people_list":{"$in":[str(user_id)]}})
        logger.info(f'The collection name is set to {collection_name}')
    
    if data.count() > 0:
        for each in data:
            people_list = find_user(each['people_list'])
            response = {
                "_id" : str(ObjectId(each['_id'])),
                "name" : each['name'],
                "people_list": [user for user in people_list['user_data']],
                "url":"http://localhost:2000/todo/" + str(ObjectId(each['_id']))
            }
        logger.info(f'The {collection_name} data were found')
        return response
    
    else:
        return None
    
    
def find_todo(title = None, ref_id = None, description = None):
    """The function is to retrive data of a todo using title or a ref_id and with or without a description
    
    Parameters
    ----------
    title : string, optional
        Has the name of the todo, by default None
    ref_id : ObjectId, optional
        The ref_id may belongs to a team or project or a company, by default None
    description : String, optional
        Additional information about the todo, by default None
    
    Returns
    -------
    json, boolean
        Return the json response that contains the information about the todo and a process status true or false
    """
    response = {}
    response["data"] = []
    
    #Finding the reference data using ref_id.
    ref_data = find_team_project_company(_id = ref_id)
    
    if (title == None) and (description == None):
        todo_data = Todo.find({"ref_id":ref_id, "delete_status": False})
    else:
        todo_data = Todo.find({"name" : title, "ref_id" : ref_id, "description" : description, "delete_status": False}) 
    
    response["ref_id"] = ref_id
    response["ref_name"] = ref_data['name']
    response["ref_url"] = ref_data['url']
    if todo_data.count() > 0:
        for todo in todo_data:
            response["data"].append({
                "_id":str(ObjectId(todo['_id'])),
                "title":todo['name'], 
                "url":"http://localhost:2000/todo/todo_list/" + str(ObjectId(todo['_id']))
            })
        return response, True
    
    else:
        return response, False


def find_todo_list(todo_id):
    """[summary]
    
    Parameters
    ----------
    todo_id : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """
    response = {}
    todo_data = Todo.find({"_id":ObjectId(todo_id), "delete_status": False})
    
    for each in todo_data:
        ref_data = find_team_project_company(_id = each['ref_id'])
        comment_data = find_comment(each['comment_list'])
        response = {
            "ref_id":each['ref_id'],
            "ref_name": ref_data['name'],
            "ref_url": ref_data['url'],
            "todo_id": str(ObjectId(each['_id'])),
            "name":each['name'],
            "description": each['description'],
            "task_details": [find_task(task_id) for task_id in each['task_list']],
            "comment_list":comment_data['data']
        }
    return response    


def find_task(task_id):
    """The function to find the task using its id.
    
    Parameters
    ----------
    task_id : ObjectId
        Holds the id of the task
    
    Returns
    -------
    json
        Returns a json response that have the details about the task belongs to the task_id
    """
    #Find task data by its id
    task_data = Task.find({"_id":ObjectId(task_id)})
    
    for data in task_data:
        assigned_to = find_user(data['assigned_to'])
        notify_to =  find_user(data['notify_to'])
        user_details = find_todo_user(data['todo_ref_id'])

        todo_data = Todo.find({"_id":ObjectId(data['todo_ref_id'])})
        for each in todo_data:
            ref_data = find_team_project_company(_id = each['ref_id'])
        
        response = {
            "ref_id":each['ref_id'],
            "ref_name": ref_data['name'],
            "ref_url": ref_data['url'],
            "todo_id": str(ObjectId(each['_id'])),
            "name":each['name'],
            "task_id": task_id,
            "description": data['description'],
            "assigned_to":[assign_users for assign_users in assigned_to['user_data']],
            "notify_to": [notify_users for notify_users in notify_to['user_data']],
            "due": data['due'],
            "user_data": user_details['user_data']
        }
    return response


def find_todo_user(todo_id):
    """The function used to find the users of a todo
    
    Parameters
    ----------
    todo_id : ObjectId
        Holds the id of the todo
    
    Returns
    -------
    json
        Contains the details about the user
    """
    todo_data = Todo.find({"_id":ObjectId(todo_id)})
    
    for data in todo_data:
        team_data = Team.find({"_id":ObjectId(data['ref_id']),"todo_list":{"$in":[str(todo_id)]}})
        project_data = Project.find({"_id":ObjectId(data['ref_id']),"todo_list":{"$in":[str(todo_id)]}})
        company_data = Company.find({"_id":ObjectId(data['ref_id']),"todo_list":{"$in":[str(todo_id)]}})
        
        if team_data.count() > 0:
            for each in team_data:
                people_list = each['people_list']
        
        elif project_data.count() > 0:    
            for each in project_data:
                people_list = each['people_list']
        else:
            for each in company_data:
                people_list = each['people_list']
        
        user_list = find_user(people_list)
    
    
    return user_list


def find_comment(id_list):
    """Function used to find the comments
    
    Parameters
    ----------
    id_list : list 
        Contains the array of comment id
    
    Returns
    -------
    json
        Has the information about comment listed and their assosiated information
    """ 

    response = {}
    response["data"] = []
    for _id in id_list:
        data = Comment.find({"_id":ObjectId(_id)})
        for each in data:
            users = find_user([each['created_by']])
            response["data"].append({
                "_id":str(ObjectId(each['_id'])),
                "created_at": each['created_at'],
                "created_by":  {
                    "person_name":users['user_data'][0]['person_name'],
                    "job_title":users['user_data'][0]['job_title']
                },
                "comment": each['comment']
            })

    return response


def find_chatroom(chatroom_id = None, company_id = None, user_id =  None):
    """The finction is ot find the chatroom using an id
    
    Parameters
    ----------
    chatroom_id : ObjectId, optional
        Hold the id of the chatroom, by default None
    company_id : ObjectId, optional
        Hold the id of the company, by default None
    user_id : ObjectId, optional
        Hold the id of the user, by default None
    
    Returns
    -------
    json
        Return the json response with the chatroom details
    """

    response = {}
    response['data'] = []
    
    if chatroom_id == None:
        chat_room_data = Chat_room.find({"company_id": company_id, "members":{"$in":[str(user_id)]}})
    else:
        chat_room_data = Chat_room.find({"_id":ObjectId(chatroom_id), "company_id": str(company_id)})
    
    for chat_data in chat_room_data:
        #Find all messages of a particular chatroom
        messages, status = find_message(chat_data['message_list'])
        members = find_user(chat_data['members'])
        response = {
            "chatroom_id":str(ObjectId(chat_data['_id'])),
            "company_id": str(chat_data['company_id']),
            "members": members['user_data'],
            "message_list": messages['data']
        }
    return response, True


def find_message(message_list):
    """The function used to find the message using the list of id of each message
    
    Parameters
    ----------
    message_list : List
        Contains the array of message ids
    
    Returns
    -------
    json, boolean
        Returns the response with the message details belong to those ids
    """
    response = {}
    response["data"] = []
    for message_id in message_list:
        message_data = Message.find({"_id":ObjectId(message_id)})
        for message in message_data:
            response["data"].append({
                "message_id": str(ObjectId(message['_id'])),
                "chat_room_id":message['chatroom_id'],
                "created_at":str(message['created_at']),
                "message":message['message'],
                "created_by": message['created_by']
            })
    return response, True