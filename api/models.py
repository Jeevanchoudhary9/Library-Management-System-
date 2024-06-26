from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    __TableName__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    password=db.Column(db.String(1024),nullable=False)
    profile_id=db.Column(db.Integer,nullable=False)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    active=db.Column(db.Boolean,nullable=False)
    role=db.Column(db.String(20),nullable=False,default="user")

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'profile_id': self.profile_id,
            'role': self.role,
        }
    
class Profile(db.Model):
    __TableName__='profile'
    profile_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False,unique=True)
    address=db.Column(db.String(100),nullable=False)
    photo=db.Column(db.String(1024))

    def serialize(self):
        return {
            'profile_id': self.profile_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'photo': self.photo
        }

class Section(db.Model):
    __TableName__='section'
    section_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    section_name=db.Column(db.String(50),nullable=False)
    date_created=db.Column(db.DateTime,nullable=False)
    description=db.Column(db.String(1024),nullable=False)

    def serialize(self):
        return {
            'section_id': self.section_id,
            'section_name': self.section_name,
            'date_created': self.date_created,
            'description': self.description
        }

class Books(db.Model):
    __TableName__='books'
    book_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    book_name=db.Column(db.String(50),nullable=False)
    author=db.Column(db.String(50),nullable=False)
    image=db.Column(db.Text,nullable=False)
    section_id=db.Column(db.Integer,nullable=False)
    date_issue=db.Column(db.DateTime)
    date_return=db.Column(db.DateTime)
    status=db.Column(db.String(10),nullable=False)
    description=db.Column(db.Text)
    title=db.Column(db.String(50))

    def serialize(self):
        return {
            'book_id': self.book_id,
            'book_name': self.book_name,
            'author': self.author,
            'section_id': self.section_id,
            'date_issue': self.date_issue,
            'date_return': self.date_return,
            'status': self.status,
            'description': self.description,
            'title': self.title
        }
    
    def short_serialize(self):
        return {
            'book_id': self.book_id,
            'book_name': self.book_name,
            'author': self.author,
            'section_id': self.section_id,
            'status': self.status,
            'title': self.title
        }
    
class History(db.Model):
    __TableName__='history'
    history_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    user_id=db.Column(db.Integer,nullable=False)
    book_id=db.Column(db.Integer,nullable=False)
    date_issue=db.Column(db.DateTime,nullable=False)
    return_date=db.Column(db.DateTime,nullable=False)
    section_id=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(20),nullable=False)

    def serialize(self):
        return {
            'history_id': self.history_id,
            'username': User.query.filter_by(id=self.user_id).first().username,
            'book_id': self.book_id,
            'book_name': Books.query.filter_by(book_id=self.book_id).first().book_name,
            'title': Books.query.filter_by(book_id=self.book_id).first().title,
            'author': Books.query.filter_by(book_id=self.book_id).first().author,
            'date_issue': self.date_issue,
            'return_date': self.return_date,
            'section_name': Section.query.filter_by(section_id=self.section_id).first().section_name,
            'status': self.status
        }

class Issue(db.Model):
    __TableName__='issue'
    issue_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    book_id=db.Column(db.Integer,nullable=False)
    user_id=db.Column(db.Integer,nullable=False)
    date_issue=db.Column(db.DateTime,nullable=False)
    return_date=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(20),nullable=False)
    # status can be 'Requested' or 'Issued' or 'Returned' or 'Completed'

    def serialize(self):
        return {
            'issue_id': self.issue_id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'date_issue': self.date_issue,
            'return_date': self.return_date,
            'status': self.status
        }
    
    def refresh():
        issue=Issue.query.all()
        for issue in issue:
            if issue.return_date<datetime.now():
                history = History(user_id=issue.user_id,book_id=issue.book_id,date_issue=issue.date_issue,return_date=issue.return_date,section_id=Books.query.filter_by(book_id=issue.book_id).first().section_id,status='Overdue')
                db.session.add(history)
                db.session.delete(issue)
        db.session.commit()
        
            

class PDF(db.Model):
    __TableName__='pdf'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    book_id = db.Column(db.Integer, nullable=False, unique=True)
    filename = db.Column(db.String(200), nullable=False)
    path = db.Column(db.Text, nullable=False)


