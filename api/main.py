from datetime import timedelta
from email.mime.text import MIMEText
from flask import Flask, render_template
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
        'check': {
            'task': 'main.check',
            'schedule': timedelta(seconds=10),
        
        }
    }
)


@celery.task()
def reminder(bind=True):
    print("Reminder Working")
    users = User.query.all()
    for user in users:

        if user.active != True and user.role != 'admin':
            print(user.username)
            print(user.role)
            profile=Profile.query.filter_by(profile_id=user.profile_id).first()
            name=profile.firstname + " " +profile.lastname
            email_message=render_template('mail_remainder.html',customer_name=name)
            
            send_email(Profile.query.filter_by(profile_id=user.profile_id).first().email, "Where are you?", email_message)

    for user in users:
        user.active = False
    db.session.commit()
    return "Reminder sent"

# @app.route('/')
# def mail_login():
#     return render_template('mail_login.html',customer_name='Rushikesh')

@app.route('/token/<token>')
def defectedlogin(token):
    user = User.query.filter_by(public_id=token).first()
    print(token,user)
    if user:
        print(user.username)
        user.public_id = "None"
        db.session.commit()
        return "Token Removed"

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