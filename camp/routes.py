import urllib
import json
import requests
from  pprint import pprint
import datetime
 
from flask_mongoengine import MongoEngine, Document
from flask import Flask, request, render_template, jsonify, Response, redirect, url_for, logging, json, flash, session
from flask.blueprints import Blueprint
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from bson.objectid import ObjectId
from flask_socketio import emit, join_room, leave_room

from camp.controller import model, mailer, create_property, update_property, search_property, delete_property
from camp import bcrypt, mail, socketio
from dynaconf import settings

api = Blueprint('CAMP', __name__)
serilaizer = URLSafeTimedSerializer('data') 

#INDEX
@api.route("/")
def home():
    return redirect(url_for("CAMP.login"))

#REGISTER
@api.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':   
        if model.User.objects(email=request.form['email']).first() is None:
            #Insert New user:
            model.User(request.form['email']).save()
            
            #Get User Id:
            user_id = model.User.objects(email=request.form['email']).first()
            user_id = ObjectId(user_id["id"])
            
            return redirect(url_for('CAMP.profile', user_id = user_id))
        else:
            flash("User already exist")
            return render_template('register.html')

    
    return render_template('register.html')

#ADMIN PROFILE
@api.route('/<user_id>/profile', methods = ['GET','POST'])
def profile(user_id):
    if request.method == 'POST':
            
        #Check use Exist
        user = model.User.objects(id=user_id).first()
        if user is not None:
            #Update user details:
            _id = ObjectId(user["id"])
            update_user = model.User.objects.get(id=_id)
            update_user.update(person_name=request.form['person_name'], job_title = request.form['job_title'])
            update_user.save()
            
            #New insert in Company details:
            model.Company(request.form['company_name'], people_list=[str(user_id)]).save()
        
            #Get Company Id:
            _id = model.Company.objects(name=request.form['company_name']).first()
            company_id = ObjectId(_id["id"])
            update_user.update(company_id = str(company_id))
            
            return redirect(url_for('CAMP.set_password', user_id = user_id, company_id = company_id))
    
    return render_template('step-1.html', user_id = user_id)


#SET PASSWORD
@api.route('/<user_id>/<company_id>/set_password', methods = ['GET','POST'])
def set_password(user_id, company_id):            
    if request.method == 'POST':        
            
        if model.User.objects(id=user_id).first() is not None:
            password = request.form['password'].encode('utf-8')
            gen_hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

            #update user details with password:
            update_password = model.User.objects.get(id=user_id)
            update_password.update(password = gen_hash_password)
            update_password.save()

            return redirect(url_for('CAMP.team', user_id = user_id, company_id = company_id))
    return render_template('step-2.html', user_id = user_id, company_id = company_id)


#CREATE TEAM WHILE ADMIN USER REGISTERS
@api.route('/<user_id>/<company_id>/team', methods=['GET', 'POST'])
def team(user_id, company_id):
    if request.method == 'POST':
        
        if model.User.objects(id=user_id).first() is not None:
            team_list = request.form.getlist('team')
            if team_list != []:
                response, status = create_property.create_team_or_project("team", team_list, company_id, user_id)
            else:
                status = True
            
            if status:
                return redirect(url_for('CAMP.projects', user_id = user_id, company_id = company_id))
            else:
                return "<h1>Failed</h1>"

    return render_template("step-3.html", user_id = user_id, company_id = company_id)


#CREATE PROJECT WHILE ADMIN USER REGISTERS
@api.route('/<user_id>/<company_id>/projects', methods=['GET', 'POST'])
def projects(user_id, company_id):
    if request.method == 'POST':
        
        if model.User.objects(id=user_id).first() is not None:
            project_list = request.form.getlist('project')
            if project_list != []:
                status = create_property.create_team_or_project( "project", project_list, company_id, user_id)
            else:
                status = True
            
            if status:
                return redirect(url_for('CAMP.invite_people', user_id = user_id, company_id = company_id))
            else:
                return "<h1>Failed</h1>"

    return render_template("step-4.html", user_id = user_id, company_id = company_id)


#INVITE PEOPLE
@api.route('/<user_id>/<company_id>/invite_people', methods=['GET', 'POST'])
def invite_people(user_id, company_id): 
    log_user = model.User.objects(id=user_id).first()   
    
    if request.method == 'POST':
        if (request.form['co_worker_email'] != "") and (request.form['co_worker_name'] != ""):
            email = request.form['co_worker_email']
            
            if log_user is not None:
                recipients = [{"email":email, "name": request.form['co_worker_name']}]
                link, token = mailer.send_mail(company_id, recipients, url = 'CAMP.invite_confirm')
                print("======================================INVITE-LINK+==========================================")
                print(link)
                print("=============================================================================================")
                
                if model.Invites.objects(co_worker_email=request.form['co_worker_email']).first() is None:
                    model.Invites(request.form['co_worker_email'], request.form['co_worker_name'], company_id, str(token)).save()
                    login_user(log_user)
                    return redirect(url_for("CAMP.dashboard", user_id = user_id))
            else:
                return "No such user exists"
        else:
            login_user(log_user)
            return redirect(url_for("CAMP.dashboard", user_id = user_id))
    
    return render_template("step-5.html",  user_id = user_id, company_id = company_id)


#CONFIRM INVITE
@api.route('/invite_confirm/<company_id>/<token>', methods = ['GET', 'POST'])
def invite_confirm(company_id, token):
    status = mailer.mail_confirmation(token)
    if status:
    
        change_status = model.Invites.objects.get(invite_id = token)
        change_status.update(invite_status = True)
        change_status.save()
        
        return redirect(url_for('CAMP.user_signup', company_id = company_id))
    else:
        return "<h2>Token Expired!</h2>"


#USER SIGNUP
@api.route('/user_signup/<company_id>')
def user_signup(company_id):
    get_company_name = model.Company.objects.get(id=company_id)
    company_name = get_company_name['name']
    return render_template('user-signup.html', company_name = company_name, company_id = company_id)


#USER DETAILS
@api.route('/user_details/<company_id>', methods = ['GET', 'POST'])
def user_details(company_id):
    get_company_name = model.Company.objects.get(id=company_id)
    company_name = get_company_name['name']
    
    if request.method == 'POST':
        check_status = search_property.check_if_exists(company_id)

        if check_status:
            password = request.form['password'].encode('utf-8')
            gen_hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
                        
            create_user = model.User(request.form['email'], gen_hash_password, request.form['person_name'], str(company_id)).save()

            #Get user id:
            _id = model.User.objects(email=request.form['email']).first()
            user_id = ObjectId(_id["id"])
            
            try:
                update_company_people_list = model.Company.objects.get(id=company_id)
                update_company_people_list.update(push__people_list=str(user_id))

            except Exception as e:
                print (e)


            return redirect(url_for('CAMP.login'))
    
    return render_template("user-details.html", company_id = company_id, company_name = company_name)


#LOGIN
@api.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for("CAMP.dashboard", user_id = current_user.id))
    if request.method == 'POST':
        user_check = model.User.objects(email = request.form['email']).first()
        if user_check:
            if bcrypt.check_password_hash(user_check['password'], request.form['password']):
                login_user(user_check)
                return redirect(url_for("CAMP.dashboard",user_id = str(ObjectId(user_check["id"]))))
    
    return render_template('login.html')


#FORGET PASSWORD
@api.route('/forget_password', methods = ['GET', 'POST'])
def forgot_password():   
    if request.method == 'POST':
        user_check = model.User.objects(email = request.form['email']).first()
        if user_check:
            link, token = mailer.send_mail(recipients = request.form['email'], url = 'CAMP.reset_confirm')
            print(link)
            model.Reset_invites(request.form['email'], user_check['company_id'], str(token)).save()
            return "Check your mail"
        else:
            return "Invalid Email Address"
    return render_template("forget_password.html")


#RESET PASSWORD CONFIRMATION
@api.route('/reset_confirm/<token>')
def reset_confirm(token):
    status = mailer.mail_confirmation(token)
    if status:
        change_status = model.Reset_invites.objects.get(reset_id = token)
        change_status.update(reset_status = True)
        change_status.save()
        return redirect(url_for("CAMP.reset_password", token = token))
    else:
        return "<h2>Token Expired!</h2>"


#EDIT PASSWORD
@api.route('/password/edit/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        user_email = model.Reset_invites.objects(reset_id = token).first()        
        if model.User.objects(email=user_email['email']).first() is not None:
            password = request.form['new_password'].encode('utf-8')
            gen_hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

            #update user details with password:
            update_password = model.User.objects.get(email=user_email['email'])
            update_password.update(password = gen_hash_password)
            update_password.save()
            return "ALL DONE"
    
    return render_template("reset_password.html", token = token)


#LOGOUT
@api.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('CAMP.login'))


#VIEW DASHBOARD
@api.route('/<user_id>/dashboard', methods = ['GET'])
@login_required
def dashboard(user_id):
    company_id = current_user.company_id
    output, status = search_property.dasboard_json(user_id, company_id)
    if status:
        return render_template("dashboard.html", output = output)
    else:
        return jsonify({"status":"No data found"})


#CREATE TEAM
@api.route('/api/team')
@login_required
def teams_creation():
    name = str(request.args.get("team_name"))
    output, status = create_property.create_team_or_project("team", [name], company_id = current_user.company_id, user_id = current_user.id)
    if status:
        return jsonify(output)
    else:
        return "<h1>Already Exist</h1>"


#CREATE PROJECT
@api.route('/api/project')
@login_required
def project_creation():
    name = request.args.get("project_name")
    output, status = create_property.create_team_or_project("project", [name], company_id = current_user.company_id, user_id = current_user.id)
    if status:
        return jsonify(output)
    else:
        return "<h1>Already Exist</h1>"


#VIEW TODO
@api.route('/todo/<ref_id>', methods=['GET', 'POST'])
def view_todo(ref_id):
    output, status = search_property.find_todo(ref_id= ref_id)
    return render_template("to-do-dashboard.html", output = output, ref_id = ref_id)


#VIEW TODO_LIST
@api.route('/todo/todo_list/<todo_id>', methods=['GET', 'POST'])
def view_todo_list(todo_id):
    output = search_property.find_todo_list(todo_id) 
    users = search_property.find_todo_user(todo_id)
    output['todo_id'] = str(todo_id) 
    output['users'] = users['user_data']
    return render_template("to-do-list.html", output = output)


#ADD TODO
@api.route('/api/add_todo', methods=['POST'])
def add_todo():
    task_data = request.get_json()
    output, todo_status = create_property.create_todo(task_data = task_data)
    if todo_status:
        return jsonify(output)
    else:
        return jsonify(output)


#CREATE TODO LIST
@api.route('/api/<todo_id>/todo_list', methods=['POST'])
def add_todo_list(todo_id):
    task_list = request.get_json()
    output = create_property.create_task(todo_id = todo_id, task_list = task_list)
    return jsonify(output) 


#VIEW TODO'S TASK
@api.route('/todo/todoset/<task_id>')
def view_task_id(task_id):
    output = search_property.find_task(task_id)
    return render_template("edit_list.html", output = output)


@api.route('/<id>/add_people')
def add_people(id):
    output = search_property.find_team_project_company(_id = id)
    company_details = search_property.find_company_data(current_user.company_id)
    output['company_peoples'] = company_details['people_list']
    return render_template("common-invite.html", output = output)


@api.route('/api/invite_user', methods=['POST'])
def add_team_project_people():
    user_data = request.get_json()
    output, status = update_property.update_user(user_data)
    if status:
        return jsonify(output)
    else:
        return jsonify({"status":"Failed", "status_code":424})


@api.route('/api/comments', methods=['GET','POST'])
def add_comments():
    data = request.get_json()
    
    comment_data = {
        "created_at": datetime.datetime.now(),
        "created_by":data['created_by'],
        "comment": str(data['comment']),
        "ref_id":data['ref_id'],   
    }
    output, status = create_property.create_comment(comment_data)
    return jsonify (output)

                   
@api.route('/api/chatroom', methods = ['POST'])
def chatroom():
    chatroom_data = request.get_json()
    users = search_property.find_user(chatroom_data['members'])
    output, status = create_property.create_chatroom(chatroom_data) 
    output['user_data'] = users['user_data']
    return jsonify(output)


@api.route('/api/message', methods = ['POST'])
def message():
    message_data = request.get_json()
    message_data['created_at'] = datetime.datetime.now()
    
    user = search_property.find_user([message_data['created_by']])    
    message_id, status = create_property.create_message(message_data)
    
    output = {
        "message_id": message_id,
        "chatroom_id": message_data['chatroom_id'],
        "created_at": str(message_data['created_at']),
        "message": message_data['message']
    }
    output['created_by'] = {
        "user_id":user['user_data'][0]['_id'],
        "person_name":user['user_data'][0]['person_name']
    }
    
    emit_message = output
    socketio.emit('message', emit_message, namespace='/chat', room=message_data['chatroom_id'])

    return jsonify(output)


@api.route('/<company_id>/chat/<chatroom_id>', methods = ['GET', 'POST'])
def view_chat_room(company_id, chatroom_id):
    session['room'] = str(chatroom_id)
    session['name'] = str(company_id)
    output, status = search_property.find_chatroom(chatroom_id=chatroom_id, company_id= company_id)
    return render_template("chat-room.html", output = output)


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)


@api.route('/api/rename', methods = ['POST'])
def name_change():
    change_details = request.get_json()
    status = update_property.update_dashboard_cards(change_details)
    if status:
        return jsonify(change_details)
    else:
        return jsonify({"error":True, "status":"Failed"})


@api.route('/api/delete', methods = ['GET','POST'])
def delete():
    card_id = request.args.get('card_id')
    todo_id = request.args.get('todo_id')
    task_id = request.args.get('task_id')

    if card_id != None:
        status = delete_property.delete_dashboard_cards(card_id)
        return jsonify({
            "status":status,
            "card_id":card_id,
        })
    
    elif todo_id != None:
        ref_id, status = delete_property.delete_todo(todo_id)
        return jsonify({
            "status":status,
            "todo_id":todo_id,
            "ref_id": ref_id
        })
    
    elif task_id != None:
        todo_id, status = delete_property.delete_task(task_id)
        return jsonify({
            "status":status,
            "task_id":task_id,
            "todo_id":todo_id
        })


@api.route('/task/edit/<task_id>', methods = ['GET','POST'])
def view_edit_task(task_id):
    input_data =  task_id
    output = search_property.find_task(input_data)
    return render_template("update.html", output = output)


@api.route('/api/edit_task', methods = ['GET','POST'])
def edit_task():
    input_data = request.get_json()
    output, status = update_property.update_task(input_data)
    return jsonify(output)


@api.route("/<user_id>/profile", methods = ['GET','POST'])
def user_profile(user_id):
    user = search_property.find_user([user_id])
    user_details = user['user_data'][0]
    return jsonify(user_details)

@api.route('/api/<user_id>/update_profile',  methods = ['GET','POST'])
def update_profile(user_id):
    input_data = request.get_json()
    input_data['user_id'] = user_id
    status = update_property.update_user_profile(input_data)
    return True

