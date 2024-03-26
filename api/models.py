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
    photo=db.Column(db.String(1024))

    def serialize(self):
        return {
            'section_id': self.section_id,
            'section_name': self.section_name,
            'date_created': self.date_created,
            'description': self.description,
            'photo': self.photo
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
    description=db.Column(db.String(1024))
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

class Issue(db.Model):
    __TableName__='issue'
    issue_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    book_id=db.Column(db.Integer,nullable=False)
    user_id=db.Column(db.Integer,nullable=False)
    date_issue=db.Column(db.DateTime,nullable=False)
    return_date=db.Column(db.DateTime,nullable=False)

class history(db.Model):
    __TableName__='history'
    history_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    user_id=db.Column(db.Integer,nullable=False)
    book_id=db.Column(db.Integer,nullable=False)
    date_issue=db.Column(db.DateTime,nullable=False)
    return_date=db.Column(db.DateTime,nullable=False)
    section_id=db.Column(db.Integer,nullable=False)


