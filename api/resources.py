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
        Issue.refresh()
        return make_response(jsonify({'status': 'Success'}), 200)
    
api.add_resource(apiCheck, '/apiCheck')


class verify_token(Resource):
    method_decorators = [token_required]

    @cross_origin()
    def get(self, current_user):
        user = User.query.filter_by(public_id=current_user.public_id).first()
        return make_response(jsonify({'message': 'Token verified successfully!', 'status': 'success','user': user.serialize()}), 200)

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

class adminDashboard(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, current_user):
        section = Section.query.all()
        section_lst=[]
        for sec in section:
            section_temp=[]
            section_temp.append(sec.serialize())
            books_temp = []
            for book in Books.query.filter_by(section_id=sec.section_id).all():
                books_temp.append(book.serialize())
            temp=[section_temp,books_temp]
            section_lst.append(temp)
        print(section_lst[0][1][0]['book_id'])
        return make_response(jsonify({'message': 'Welcome to the admin\'s dashboard!','user_data': current_user.serialize(),'section': section_lst, 'status': 'success'}), 200)

                
api.add_resource(adminDashboard, '/admin_dashboard')

class Book(Resource):
    method_decorators = {'get': [token_required]}
    def get(self,current_user,book_id):
        book_obj = Books.query.filter_by(book_id=book_id).first()
        books=Books.query.filter_by(section_id=book_obj.section_id).all()
        try:
            issue=Issue.query.filter_by(book_id=book_id, user_id=current_user.id).first().status
        except:
            issue=None
        books_lst=[]
        for book in books:
            if book.book_id != book_id:
                books_lst.append(book.serialize())
        if book_obj:
            return make_response(jsonify({'current_book': book_obj.serialize(),'issue': issue,'user_data': current_user.serialize(), 'status': 'success','books': books_lst}), 200)
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
        if len(data['description'].split())>300 or sum(c.isalpha() for c in data['description']) >1600:
            return make_response(jsonify({'message': 'Description should not exceed 300 words or 1600 characters', 'status': 'error'}), 400)
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
    method_decorators = {'post': [token_required]}

    def post(self, current_user):
        data = request.json
        print(data)
        try:
            if data['section_name'] == "" or data['description'] == "":
                return make_response(jsonify({'message': 'All fields are required', 'status': 'error'}), 400)
            if len(data['description'].split())>300 or sum(c.isalpha() for c in data['description']) >1600:
                return make_response(jsonify({'message': 'Description should not exceed 300 words or 1600 characters', 'status': 'error'}), 400)
            if Section.query.filter_by(section_name=data['section_name']).first():
                return make_response(jsonify({'message': 'Section already exists', 'status': 'error'}), 409)
        except Exception as e:
            return make_response(jsonify({'message': str(e), 'status': 'error'}), 400)
        try:
            section = Section(section_name=data['section_name'], date_created=datetime.now(), description=data['description'])
            db.session.add(section)
            db.session.commit()
            return make_response(jsonify({'message': 'Section added successfully', 'status': 'success'}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
        
api.add_resource(AddSection, '/add_section')

class EditSection(Resource):
    method_decorators = {'post': [token_required]}

    def post(self, current_user):
        data = request.json
        try:
            section = Section.query.filter_by(section_id=data['section_id']).first()
            if section:
                section.section_name = data['section_name']
                section.description = data['description']
                db.session.commit()
                return make_response(jsonify({'message': 'Section updated successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Section not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
        
api.add_resource(EditSection, '/edit_section')

class DeleteSection(Resource):
    method_decorators = {'post': [token_required]}

    def post(self, current_user):
        data = request.json
        try:
            section = Section.query.filter_by(section_id=data['section_id']).first()
            if section:
                db.session.delete(section)
                db.session.commit()
                return make_response(jsonify({'message': 'Section deleted successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Section not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(DeleteSection, '/delete_section')

class RequestBook(Resource):
    method_decorators = {'post': [token_required]}
    
    def post(self, current_user):
        data = request.json
        try:
            if Issue.query.filter_by(user_id=current_user.id, book_id=data['book_id'], status='Requested').first():
                issue = Issue.query.filter_by(user_id=current_user.id, book_id=data['book_id'], status='Requested').first()
                try:
                    data['period']=int(data['period'])
                except:
                    return make_response(jsonify({'message': 'Invalid period', 'status': 'error'}), 400)
                if data['book_id'] == "" or data['period'] == "" or data['unit'] == "":
                    return make_response(jsonify({'message': 'All fields are required', 'status': 'error'}), 400)
                if data['unit']=='hrs':
                    if data['period'] > 672:
                        return make_response(jsonify({'message': 'Period should not be more than 4 weeks', 'status': 'error'}), 400)
                    return_date = datetime.now() + timedelta(hours=data['period'])
                elif data['unit']=='days':
                    if data['period'] > 28:
                        return make_response(jsonify({'message': 'Period should not be more than 4 weeks', 'status': 'error'}), 400)
                    return_date = datetime.now() + timedelta(days=data['period'])
                elif data['unit']=='weeks':
                    if data['period'] > 4:
                        return make_response(jsonify({'message': 'Period should not be more than 4 weeks', 'status': 'error'}), 400)
                    return_date = datetime.now() + timedelta(weeks=data['period'])
                else:
                    return make_response(jsonify({'message': 'Invalid unit', 'status': 'error'}), 400)
                issue.return_date = return_date
                issue.status = 'Requested'
                db.session.commit()


                return make_response(jsonify({'message': 'Your Request for edit is successful', 'status': 'success'}), 200)
            if Issue.query.filter_by(user_id=current_user.id).count() >= 5:
                return make_response(jsonify({'message': 'You have reached the maximum limit of 5 books', 'status': 'error'}), 400)
            print(current_user)
            print(data)
            print(data['book_id'],data['period'],data['unit'])
            try:
                data['period']=int(data['period'])
            except:
                return make_response(jsonify({'message': 'Invalid period', 'status': 'error'}), 400)
            
            if data['book_id'] == "" or data['period'] == "" or data['unit'] == "":
                return make_response(jsonify({'message': 'All fields are required', 'status': 'error'}), 400)
            if data['unit']=='hrs':
                if data['period'] > 672:
                    return make_response(jsonify({'message': 'Period should not be more than 4 weeks', 'status': 'error'}), 400)
                return_date = datetime.now() + timedelta(hours=data['period'])
            elif data['unit']=='days':
                if data['period'] > 28:
                    return make_response(jsonify({'message': 'Period should not be more than 4 weeks', 'status': 'error'}), 400)
                return_date = datetime.now() + timedelta(days=data['period'])
            elif data['unit']=='weeks':
                if data['period'] > 4:
                    return make_response(jsonify({'message': 'Period should not be more than 4 weeks', 'status': 'error'}), 400)
                return_date = datetime.now() + timedelta(weeks=data['period'])
            else:
                return make_response(jsonify({'message': 'Invalid unit', 'status': 'error'}), 400)
            
            print(return_date)
            
            issue = Issue(book_id=data['book_id'], user_id=current_user.id, date_issue=datetime.now(), return_date=return_date, status='Requested')
            db.session.add(issue)
            db.session.commit()
            return make_response(jsonify({'message': 'Request sent successfully', 'status': 'success'}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(RequestBook, '/request_book')

class CancelRequest(Resource):
    method_decorators = {'post': [token_required]}
    
    def post(self, current_user):
        data = request.json
        try:
            issue = Issue.query.filter_by(user_id=current_user.id, book_id=data['book_id'], status='Requested').first()
            if issue:
                db.session.delete(issue)
                db.session.commit()
                return make_response(jsonify({'message': 'Request cancelled successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Request not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
    
api.add_resource(CancelRequest, '/cancel_request')

class RequestedBooks(Resource):
    method_decorators = {'get': [token_required]}

    def get(self,current_user, status):
        issues = Issue.query.filter_by(user_id=current_user.id).all()
        issues_lst = []
        books_lst = []
        for issue in issues:
            if issue.status == status:
                issue_temp =[issue.serialize()]
                issue_temp.append(Books.query.filter_by(book_id=issue.book_id).first().short_serialize())
                issues_lst.append(issue_temp)
        return make_response(jsonify({'requested_books': issues_lst, 'status': 'success', 'current_user': current_user.serialize()}), 200)

api.add_resource(RequestedBooks, '/requested_books/<string:status>')

class ReturnBook(Resource):
    method_decorators = {'post': [token_required]}

    def post(self,current_user):
        data = request.json
        try:
            issue = Issue.query.filter_by(user_id=current_user.id, book_id=data['book_id'], status='Issued').first()
            if issue:
                db.session.delete(issue)
                history = History(book_id=data['book_id'], user_id=current_user.id, date_issue=issue.date_issue, return_date=datetime.now(),status='Returned',section_id=Books.query.filter_by(book_id=data['book_id']).first().section_id)
                db.session.add(history)
                db.session.commit()
                return make_response(jsonify({'message': 'Book returned successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Book not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(ReturnBook, '/return_book')

class CancelAllRequests(Resource):
    method_decorators = {'post': [token_required]}
    
    def post(self, current_user):
        try:
            issues = Issue.query.filter_by(user_id=current_user.id, status='Requested').all()
            for issue in issues:
                db.session.delete(issue)
                db.session.commit()
            return make_response(jsonify({'message': 'All requests cancelled successfully', 'status': 'success'}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
    
api.add_resource(CancelAllRequests, '/cancel_all_requests')

class ReturnAllBooks(Resource):
    method_decorators = {'post': [token_required]}

    def post(self,current_user):
        try:
            issues = Issue.query.filter_by(user_id=current_user.id, status='Issued').all()
            for issue in issues:
                history = History(book_id=issue.book_id, user_id=current_user.id, date_issue=issue.date_issue, return_date=datetime.now(),status='Returned',section_id=Books.query.filter_by(book_id=issue.book_id).first().section_id)
                db.session.delete(issue)
                db.session.add(history)
                db.session.commit()
            return make_response(jsonify({'message': 'All books returned successfully', 'status': 'success'}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
        
api.add_resource(ReturnAllBooks, '/return_all_books')

class HistoryBooks(Resource):
    method_decorators = {'get': [token_required]}

    def get(self,current_user):
        history = History.query.filter_by(user_id=current_user.id).all()
        history_lst = []
        for h in history:
            history_lst.append(h.serialize())
        return make_response(jsonify({'history': history_lst, 'status': 'success'}), 200)
    
api.add_resource(HistoryBooks, '/history')