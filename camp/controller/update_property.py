from bson.objectid import ObjectId

from dynaconf import settings
from camp.controller import search_property

from camp.controller.mongo_collections import db, User, Company, Team, Project, Todo, Task, Comment, Chat_room, Message


def update_user_profile(input_data):
    """Update the user information
    
    Parameters
    ----------
    input_data : json
        Contain the data of user details that need to be update.
    
    Returns
    -------
    boolean
        Return True or False 
    """
    User.update({
        "_id": ObjectId(input_data['user_id'])}, 
        {"$set":{
            "email": input_data['email'], 
            "job_title": input_data['job_title'], 
            "person_name": input_data['person_name']
        }
    })
    return True


def update_dashboard_cards(input_data):
    """[summary]
   
    Parameters
    ----------
    input_data : json
        Contain name and id , that need to be change
   
    Returns
    -------
    boolean
       Give the process status success or not by true or false
   """

    collections = ['team', 'project', 'todo']
    for collection in collections:
        data = db[collection].find({"_id":ObjectId(input_data['_id'])})
        if data.count() > 0:
            db[collection].update({
                "_id":ObjectId(input_data['_id'])}, 
                {"$set":{"name":input_data['name']}})
    
    return True


def update_task(input_data):
    """[summary]
    
    Parameters
    ----------
    input_data : json
        Contains the data about task details that needs to be updated. 
    
    Returns
    -------
    json, boolean
        Return the output json and a true status when the process get success
    """
    Task.update({
        "_id": ObjectId(input_data['_id'])},
        {
            "$set":{"description" : input_data['description'],
	                "assigned_to" : input_data['assigned_to'],
	                "notify_to" : input_data['notify_to'],
	                "due" : input_data['due']}
                    })
    output = search_property.find_task(input_data['_id'])
    return output, True


def update_company_data(collection_name, member_list, name, company_id, user_id):
    """[summary]
    
    Parameters
    ----------
    collection_name : string
        name of the collection need to be updated
    member_list : list
        contain the people name 
    name : string
        name of the team or project
    company_id : ObjectId
        Id of the company
    user_id : ObjectId
        Id of the user
    
    Returns
    -------
    Boolean
        Returns true or false
    """
    collection_data = db[collection_name].find({"name":name, "company_id":company_id, "people_list":{"$in":[str(user_id)]}})
    for data in collection_data:
        people_id = ObjectId(data['_id'])
    
    if Company.count_documents({"_id":ObjectId(company_id), member_list:{"$in":[str(people_id)]}}) > 0:
        pass
    else:
        Company.update({"_id":ObjectId(company_id)},{"$push":{member_list:str(people_id)}})
    
    return True


def update_user(user_data):
    """[summary]
    
    Parameters
    ----------
    user_data : json
        contains the data of user that need to be updated
    
    Returns
    -------
    json, boolean
        return the updated user data and a process status as true
    """
    
    if Team.count({"_id":ObjectId(user_data['id'])}) > 0:     
        if Team.count({"_id":ObjectId(user_data['id']), "people_list":{"$in":[str(user_data['people_id'])]}}) > 0:
            update_user_data = search_property.find_user([user_data['people_id']])
            return update_user_data['user_data'][0], True
        
        else:
            Team.update({"_id":ObjectId(user_data['id'])}, {"$push":{"people_list": str(user_data['people_id'])}})
    
    else:    
        if Project.count({"_id":ObjectId(user_data['id']), "people_list":{"$in":[str(user_data['people_id'])]}}) > 0:
            update_user_data = search_property.find_user([user_data['people_id']])
            return update_user_data['user_data'][0], True
        
        else:
            Project.update({"_id":ObjectId(user_data['id'])}, {"$push":{"people_list": str(user_data['people_id'])}})
    
    update_user_data = search_property.find_user([user_data['people_id']])
    return update_user_data['user_data'][0], True