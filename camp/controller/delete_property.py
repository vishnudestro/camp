from bson.objectid import ObjectId
import logging

from dynaconf import settings
from camp.controller import search_property

from camp.controller.mongo_collections import db, User, Company, Team, Project, Todo, Task, Comment, Chat_room, Message

logger = logging.getLogger(__name__)

def delete_dashboard_cards(_id):
    """The function is to delete the dashboard card(team or project).
    
    Parameters
    ----------
    _id : string
        Get the id's of team or project to that needs to be deleted.
    
    Returns
    -------
    boolean
        Give the process status success or not by true or false.
    """

    collections = ['team', 'project']
    #Check whether the given id belongs to a team or project.
    for collection in collections:
        data = db[collection].find({"_id":ObjectId(_id)})
        
        #If the data for the is id is exist update the delete status as True.
        if data.count() > 0:
            update_list = collection + "_list"
            db[collection].update({
                "_id":ObjectId(_id)}, 
                {"$set":{"delete_status": True}})
            logger.info(f'The {collection} id: {_id} is removed')
                
            
            #update the company data by pulling the corresponding team or project id from their list.
            for each in data:
                Company.update({"_id":ObjectId(each['company_id'])},{"$pull":{update_list: str(_id)}})
    
    return True


def delete_todo(_id):
    """The funtion is to delete the todo.
    
    Parameters
    ----------
    _id : string
        Get the todo id to change the delete status to True
    
    Returns
    -------
    boolean
        Give the process status success or not by true or false
    """
    #Find the todo data that want to be deleted.
    data = Todo.find({"_id":ObjectId(_id)})
    
    #If the data exist
    if data.count() > 0:
        #Update the delete status as true.
        Todo.update({
            "_id":ObjectId(_id)}, 
            {"$set":{"delete_status": True}})
        logger.info(f'The todo id: {_id} is removed')
        
        #Once the status get updated pull the todo id from the team or the project the id belongs to.
        for each in data:
            #If the id belongs to a team.
            if Team.count({"_id":ObjectId(each['ref_id'])}) > 0:
                Team.update({"_id":ObjectId(each['ref_id'])},{"$pull":{'todo_list': str(_id)}})
            
            #If a id belongs to project.
            else:
                Project.update({"_id":ObjectId(each['ref_id'])},{"$pull":{'todo_list': str(_id)}})
    
    return each['ref_id'], True


def delete_task(_id):
    """The delete the task and their related data's
    
    Parameters
    ----------
    _id : string
        Get the task id to change the delete status to True
    
    Returns
    -------
    boolean
        give the process status success or not by true or false
    """
    
    #Find the task data that want to be deleted.
    data = Task.find({"_id":ObjectId(_id)})
    
    #If the data exist
    if data.count() > 0:
        #Update the delete status as true.
        Task.update({
            "_id":ObjectId(_id)}, 
            {"$set":{"delete_status": True}})
        logger.info(f'The task id: {_id} is removed')
        
        #Once the status get updated pull the task id from the todo's task list.
        for each in data:
            Todo.update({
                "_id":ObjectId(each['todo_ref_id'])},
                {"$pull":{'task_list': str(_id)}})

    return each['todo_ref_id'], True