from datetime import timedelta
from email.mime.text import MIMEText
from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS
from flask_restful import Api, Resource
import weasyprint 
from models import Books, History, Section, db, User
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
        'mail_pdf_report_admin': {
            'task': 'main.mail_pdf_report_admin',
            'schedule': crontab(hour=12, minute=00, day_of_month=1),
        },
        # 'check': {
        #     'task': 'main.check',
        #     'schedule': timedelta(seconds=10),
        
        # }
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

def mail_pdf_report(id):
    current_user=User.query.filter_by(id=id).first()
    print(current_user.id)
    books=Books.query.all()
    books_lst=[]
    sections_lst=[]
    status_lst=[]
    temp={}
    for book in books:
        temp=[]
        if History.query.filter_by(book_id=book.book_id,user_id=current_user.id).count()!=0:
            temp.append(book.book_name)
            temp.append(History.query.filter_by(book_id=book.book_id,user_id=current_user.id).count())
            books_lst.append(temp)
    for section in Section.query.all():
        temp=[]
        if History.query.filter_by(section_id=section.section_id,user_id=current_user.id).count()!=0:
            temp.append(section.section_name)
            temp.append(History.query.filter_by(section_id=section.section_id,user_id=current_user.id).count())
            sections_lst.append(temp)
    for books in History.query.with_entities(History.status).distinct().all():
        temp=[]
        temp.append(books.status)
        temp.append(History.query.filter_by(status=books.status,user_id=current_user.id).count())
        status_lst.append(temp)
    
    data={'books_lst': books_lst, 'status': 'success','current_user': current_user.serialize(),'sections_lst': sections_lst,'status_lst':status_lst}


    rendered = render_template('user_report.html',data=data)
    pdf = weasyprint.HTML(string=rendered).write_pdf()
    email=Profile.query.filter_by(profile_id=current_user.profile_id).first().email
    send_email(email, "PDF Report", "rendered", attachment=pdf)
    return rendered

@celery.task()
def mail_pdf_report_admin():
    current_user=User.query.filter_by(role="admin").first()
    print(current_user.id)
    books=Books.query.all()
    books_lst=[]
    sections_lst=[]
    status_lst=[]
    temp={}
    for book in books:
        temp=[]
        temp.append(book.book_name)
        temp.append(History.query.filter_by(book_id=book.book_id).count())
        books_lst.append(temp)

    for section in Section.query.all():
        temp=[]
        temp.append(section.section_name)
        temp.append(History.query.filter_by(section_id=section.section_id).count())
        sections_lst.append(temp)
    for books in History.query.with_entities(History.status).distinct().all():
        temp=[]
        temp.append(books.status)
        temp.append(History.query.filter_by(status=books.status).count())
        status_lst.append(temp)
    
    data={'books_lst': books_lst, 'status': 'success','current_user': current_user.serialize(),'sections_lst': sections_lst,'status_lst':status_lst}


    rendered = render_template('user_report.html',data=data)
    pdf = weasyprint.HTML(string=rendered).write_pdf()
    email=Profile.query.filter_by(profile_id=current_user.profile_id).first().email
    send_email(email, "PDF Report", "rendered", attachment=pdf)
    return rendered

@celery.task()
def monthly_report():
    print("Monthly Report Working")
    users = User.query.all()
    for user in users:
        if user.role != 'admin':
            mail_pdf_report(user.id)
    return "Monthly Report Sent"

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
# api=Api(prefix='/api')
@app.route('/api/usersummary_pdf/<int:user_id>')
def get(user_id):
    
    current_user=User.query.filter_by(id=user_id).first()
    if current_user.role == 'admin':
        return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
    books=Books.query.all()
    books_lst=[]
    books_count=[]
    sections_count=[]
    sections_name=[]
    status_count=[]
    status_name=[]
    for book in books:
        if History.query.filter_by(book_id=book.book_id,user_id=current_user.id).count()!=0:
            books_lst.append(book.book_name)
            books_count.append(History.query.filter_by(book_id=book.book_id,user_id=current_user.id).count())
    for section in Section.query.all():
        if History.query.filter_by(section_id=section.section_id,user_id=current_user.id).count()!=0:
            sections_name.append(section.section_name)
            sections_count.append(History.query.filter_by(section_id=section.section_id,user_id=current_user.id).count())
    for books in History.query.all():
        if books.status in status_name:
            continue
        status_name.append(History.query.filter_by(status=books.status,user_id=current_user.id).first().status)
        status_count.append(History.query.filter_by(status=books.status,user_id=current_user.id).count())
    
    # return make_response(jsonify({'books': books_lst, 'books_count': books_count, 'status': 'success','current_user': current_user.serialize(),'sections_count': sections_count,'sections_name': sections_name,'status_name':status_name,'status_count':status_count}), 200)
# api.add_resource(UserSummaryPDF, '/usersummary_pdf/<int:user_id>')


if __name__ == '__main__':
    app.run(debug=True)