from camp import mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message
from flask import url_for

from dynaconf import settings
from camp.controller.mongo_collections import Invites


#Serializer secret Key
serilaizer = URLSafeTimedSerializer('data')

def send_mail(company_id = None, recipients = None, url = None, type = None):    
    #TODO: check with sender and receiver mail from default
    
    token = serilaizer.dumps(recipients, salt='email-confirm')
    # msg = Message('Confirm email', sender='vishnu@positivenaick.com', recipients=["prakashvishnu45@gmail.com"])
    if url == 'CAMP.invite_confirm':
        link = url_for(url, company_id=company_id, token=token, _external=True)
    else:
        link = url_for(url, token=token, _external=True)
    # msg.body = "Your link as follows: {}".format(link)
    # mail.send(msg)

    return link, token

def mail_confirmation(token):
    try:
        if Invites.count_documents({"invite_id":str(token), "invite_status" : False}) > 0:
            email = serilaizer.loads(token, salt='email-confirm', max_age=900)
        else:
            return False
    except SignatureExpired:
        return False
    
    return True
