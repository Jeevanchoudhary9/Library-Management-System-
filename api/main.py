from datetime import timedelta
from email.mime.text import MIMEText
from flask import Flask
from flask_cors import CORS 
from models import db, User
from config import DevelopmentConfig, celeryConfig
from resources import api
from email.mime.multipart import MIMEMultipart
from flask_mail import Mail,Message
from celery.schedules import crontab

# def create_app():
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(DevelopmentConfig)
db.init_app(app)
api.init_app(app)

# # commented today from below

from resources import send_email, Profile




from celerywork import make_celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_BACKEND'] = 'redis://localhost:6379/2'

celery=make_celery(app)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    beat_schedule={
        'reminder': {
            'task': 'main.reminder',
            'schedule': crontab(hour=12, minute=00),
            # 'schedule': timedelta(seconds=10),
        },
        'monthly_report': {
            'task': 'main.monthly_report',
            'schedule': crontab(hour=12, minute=00, day_of_month=1),
        },
    }
)


@celery.task()
# @app.route('/')
def reminder(bind=True):
    print("Reminder Working")
    users = User.query.all()
    for user in users:

        if user.active != True and user.role != 'admin':
            text = "How long are you going to be away?\n" + "We miss you. Please give us a visit \n\nThank you."
            # send_email(Profile.query.filter_by(profile_id=user.profile_id).first().email, "Where are you?", text)

        if user.active == True: 
            user.active = False

    for user in users:
        user.active = False
    return "Reminder sent"

# @app.route('/process/<name>')
# def process(name):
#     return name

# @celery.task()
# def reverse(string):
#     return string[::-1]

# @celery.task()
# def hellos():
#     print("Hello World")
#     return "Hello"

if __name__ == '__main__':
    app.run(debug=True)