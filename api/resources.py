import base64
from functools import wraps
import os
import uuid
from flask import Response, app, jsonify, make_response, request, send_file
from flask_cors import cross_origin
from flask_restful import Resource, Api, reqparse,fields,marshal_with
from models import db
from models import *
import jwt
from config import DevelopmentConfig
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,check_password_hash


api=Api(prefix='/api')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if request.headers.get('x-access-token'):
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'Token is missing!'}), 401)
        try:
            data = jwt.decode(
                token, DevelopmentConfig.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return make_response(jsonify({'message': 'Token is invalid!'}), 401)
        return f(current_user, *args, **kwargs)
    return decorated


class apiCheck(Resource):

    # Check API
    @cross_origin()
    def get(self):
        return make_response(jsonify({'status': 'Success'}), 200)
    
api.add_resource(apiCheck, '/apiCheck')


class verify_token(Resource):
    method_decorators = [token_required]

    @cross_origin()
    def get(self, current_user):
        return make_response(jsonify({'message': 'Token verified successfully!', 'status': 'success'}), 200)

api.add_resource(verify_token, '/verify_token')


class Register(Resource):

    # Register a new user
    def post(self):
        data = request.json
        # match user by username or email
        user = User.query.filter_by(username=data['username']).first()
        data['phone_number']=str(data['phone_number'])
        try:
            if user:
                return make_response(jsonify({'message': 'User already exists', 'status': 'error'}), 409)
            else:
                if data['firstname'] == "" or data['lastname'] == "" or data['username'] == "" or data['password'] == "" or data['phone_number'] == "" or data['address'] == "" or data['email'] == "":
                    return make_response(jsonify({'message': 'All fields are required or Type is invalid', 'status': 'error'}), 400)
                # elif data['phone_number'].isdigit() == False:
                #     return make_response(jsonify({'message': 'Invalid phone number', 'status': 'error'}), 400)
                elif Profile.query.filter_by(email=data['email']).first():
                    return make_response(jsonify({'message': 'Email already exists', 'status': 'error'}), 409)
                elif data['password'] != data['confirm_password']:
                    return make_response(jsonify({'message': 'Passwords do not match', 'status': 'error'}), 400)
                elif data['password'] == data['username']:
                    return make_response(jsonify({'message': 'Password cannot be the same as username', 'status': 'error'}), 400)
                elif data['email'].find('@') == -1 or data['email'].find('.') == -1:
                    return make_response(jsonify({'message': 'Invalid email', 'status': 'error'}), 400)
                if data['photo']=='':
                    photo=None
                else:
                    photo=data['photo']

                try:
                    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
                    profile = Profile(firstname=data['firstname'], lastname=data['lastname'], phone=data['phone_number'], email=data['email'], address=data['address'], photo=photo)
                    db.session.add(profile)
                    db.session.commit()
                    user = User(username=data['username'], password=hashed_password, public_id=str(uuid.uuid4()), active=True, role='user', profile_id=Profile.query.filter_by(email=data['email']).first().profile_id)
                    db.session.add(user)
                    db.session.commit()
                    return make_response(jsonify({'message': 'User registered successfully','status': 'success'}), 201)
                except Exception as e:
                    db.session.rollback()
                    return make_response(jsonify({'error': str(e)}), 500)
                
        except:
            return make_response(jsonify({'message': 'Error!', 'status': 'error'}), 400)
        

api.add_resource(Register, '/register')


class Login(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, current_user):
        user = User.query.filter_by(public_id=current_user.public_id).first()
        return make_response(jsonify({'message': current_user, 'status': 'success'}), 200)

    # Login a user and obtain JWT token
    def post(self):
        auth = request.json
        username = auth['username']
        password = auth['password']
        if not username or not password:
            return make_response(jsonify({'message': 'Please enter all fields!', 'status': 'error'}), 401)
        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response(jsonify({'message': 'User does not exist!', 'status': 'error'}), 404)
        if check_password_hash(user.password, password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow(
            ) + timedelta(minutes=30)}, DevelopmentConfig.SECRET_KEY, algorithm="HS256")
            return make_response(jsonify({'token': token, 'user_data': user.serialize(), 'status': 'success'}), 200)
        return make_response(jsonify({'message': 'Incorrect password!', 'status': 'error'}), 401)

api.add_resource(Login, '/login')

class Dashboard(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, current_user):
        books = Books.query.all()
        books_lst=[]
        for book in books:
            books_lst.append(book.serialize())

        books_lst_section = []
        sections = Section.query.all()
        for section in sections:
            books=Books.query.filter_by(section_id=section.section_id).all()
            books_temp=[]
            for book in books:
                temp = book.serialize()
                temp['section_name'] = section.section_name
                books_temp.append(temp)
            books_lst_section.append(books_temp)

        return make_response(jsonify({'message': 'Welcome to the dashboard!','user_data': current_user.serialize(),'books': books_lst,'books_lst_section':books_lst_section, 'status': 'success'}), 200)

api.add_resource(Dashboard, '/dashboard')

class Book(Resource):
    method_decorators = {'get': [token_required]}

    def get(self,current_user,book_id):
        book_obj = Books.query.filter_by(book_id=book_id).first()
        if book_obj:
            return make_response(jsonify({'books': book_obj.serialize(),'user_data': current_user.serialize(), 'status': 'success'}), 200)
        return make_response(jsonify({'message': 'Book not found!', 'status': 'error'}), 404)

api.add_resource(Book, '/book/<int:book_id>')

class fetchbookimg(Resource):
    def get(self, book_id):
        book = Books.query.filter_by(book_id=book_id).first()
        if book:
            print("ok")
            return Response(book.image, mimetype="image/jpeg")
        return make_response(jsonify({'message': 'Book not found!', 'status': 'error'}), 404)
    
api.add_resource(fetchbookimg, '/fetchbookimg/<int:book_id>')


class AddBooks(Resource):
    def post(self):
        
        data = request.json
        try:
            date_issue = datetime.now()
            book = Books(book_name=data['book_name'], author=data['author'], image=data['image'], section_id=data['section_id'],date_issue=date_issue, status=data['status'], description=data['description'], title=data['title'])
            db.session.add(book)
            db.session.commit()
            return make_response(jsonify({'message': 'Book added successfully', 'status': 'success'}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
        
api.add_resource(AddBooks, '/add_books')

class uploaddata(Resource):
    def post(self):

        if request.files:
            # Handle file upload
            image_file = request.files['image']
            image_data = image_file.read()
            # Handle form data
            try:
                date_issue = datetime.now()
                book_data = request.form
                
                book = Books(
                    book_name=book_data['book_name'],
                    author=book_data['author'],
                    image=image_data,  # If image is part of form data
                    section_id=book_data['section_id'],
                    date_issue=date_issue,
                    status=book_data['status'],
                    description=book_data['description'],
                    title=book_data['title']
                )
                
                db.session.add(book)
                db.session.commit()
                return make_response(jsonify({'message': 'Book added successfully', 'status': 'success'}), 201)
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(uploaddata, '/addbooks')


class AddSection(Resource):
    def post(self):
        data = request.json
        try:
            section = Section(section_name=data['section_name'], date_created=datetime.now(), description=data['description'], photo=data['photo'])
            db.session.add(section)
            db.session.commit()
            return make_response(jsonify({'message': 'Section added successfully', 'status': 'success'}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
        
api.add_resource(AddSection, '/add_section')