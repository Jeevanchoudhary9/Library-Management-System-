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

# # commented today from below

# celery = Celery("Application Jobs")
# HOST = 'localhost'
# PORT = 6379
# celery.conf.update(
#     broker_url='redis://{}:{}/{}'.format(HOST, PORT, 1),
#     result_backend='redis://{}:{}/{}'.format(HOST, PORT, 2),
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='Asia/Kolkata',
#     enable_utc=True,
#     beat_schedule={
#         'reminder': {
#             'task': 'main.reminder',
#             'schedule': crontab(hour=12, minute=00),
#         },
#         'monthly_report': {
#             'task': 'main.monthly_report',
#             'schedule': crontab(hour=12, minute=00, day_of_month=1),
#         }
#     }
# )

# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

from resources import send_email, Profile

# @celery.task()
# def hellos():
#     print("Hello World")
#     return "Hello"

# @celery.task()
# # @app.route('/')
# def reminder(bind=True):
#     users = User.query.all()
#     for user in users:

#         if user.active != True and user.role != 'admin':
#             text = "How long are you going to be away?\n" + "We miss you. Please give us a visit \n\nThank you."
#             send_email(Profile.query.filter_by(profile_id=user.profile_id).first().email, "Where are you?", text)

#         if user.active == True: 
#             user.active = False

#     for user in users:
#         user.active = False
#     return "Reminder sent"



if __name__ == '__main__':
    app.run(debug=True)