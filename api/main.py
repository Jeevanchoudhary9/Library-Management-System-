from datetime import timedelta
from email.mime.text import MIMEText
from flask import Flask
from flask_cors import CORS 
from models import db, User
from config import DevelopmentConfig
from resources import api
from email.mime.multipart import MIMEMultipart
from celery import Celery
from celery.schedules import crontab
from flask_mail import Mail,Message

# def create_app():
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(DevelopmentConfig)
db.init_app(app)
api.init_app(app)

# Usage example
# receiver_email = 'jeevanchoudhary2421@gmail.com'
# subject = 'Monthly Report'
# message = 'mmmmm\n\nRegards,\nLibrary Management System'

# send_email(receiver_email, subject, message)


# SMTP_SERVER_HOST = 'localhost'
# SMTP_SERVER_PORT = 1025
# SENDER_ADDRESS = 'admin@librarymanagementsystem.co.in'
# SENDER_PASSWORD = ''


# def send_email(to, subject, body):
#     msg = MIMEMultipart()
#     msg['Subject'] = subject
#     msg['From'] = SENDER_ADDRESS
#     msg['To'] = to
#     msg.attach(MIMEText(body, 'html'))
#     server = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
#     server.login(SENDER_ADDRESS, SENDER_PASSWORD)
#     server.send_message(msg)
#     server.quit()
#     return True

@app.route('/')
def reminder(bind=True):
    users = User.query.all()
    for user in users:
        if user.active == True: 
            user.active = False
        else:
            user.active = True
            
        if user.active != True and user.role != 'admin':
            text = "How long are you going to be away?\n" + "We miss you. Please give us a visit \n\nThank you."
            send_email(Profile.query.filter_by(profile_id=user.profile_id).first().email, "Where are you?", text)
    for user in users:
        user.active = False
    send_email('jeevanchoudhary2421@gmail.com', "Where are you?", "text")
    return "Reminder sent"


celery = Celery("Application Jobs")
HOST = 'localhost'
PORT = 6379
celery.conf.update(
    broker_url='redis://{}:{}/{}'.format(HOST, PORT, 0),
    result_backend='redis://{}:{}/{}'.format(HOST, PORT, 0),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    beat_schedule={
        'reminder': {
            'task': 'main.reminder',
            # 'schedule': crontab(hour=12, minute=00),
            'schedule': timedelta(seconds=10),
        }
    }
)

# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

from resources import send_email, Profile

# @celery.task()


if __name__ == '__main__':
    app.run(debug=True)
    