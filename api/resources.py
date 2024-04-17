import base64
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
import os
import random
import threading
import uuid
import smtplib
from flask import Response, app, jsonify, make_response, render_template, request, send_file
from flask_cors import cross_origin
from flask_restful import Resource, Api, reqparse,fields,marshal_with
from models import db
from models import *
import jwt
from config import DevelopmentConfig
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,check_password_hash
import json
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

api=Api(prefix='/api')

def send_email(to_email, subject, html_content,attachment=None):
    # Gmail SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Gmail SMTP port

    # Sender's Gmail address and password
    sender_email = 'jeevanchoudhary2421@gmail.com'
    sender_password = 'sdyo knaw zkgj kvkd'

    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    if attachment:
        # Attach file
        # part = MIMEBase('application', 'octet-stream')
        # part.set_payload(open(attachment, 'rb').read())
        # encoders.encode_base64(part)
        # part.add_header('Content-Disposition', f'attachment; filename={attachment}')
        # msg.attach(part)

        pdf_part = MIMEApplication(attachment, _subtype='pdf')
        pdf_part.add_header('Content-Disposition', 'attachment', filename='report.pdf')
        msg.attach(pdf_part)


    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html','utf-8'))

    

    # Connect to Gmail's SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption
    server.login(sender_email, sender_password)  # Login to Gmail

    # Send email
    server.sendmail(sender_email, to_email, msg.as_string())

    # Close SMTP connection
    server.quit()


# # from main import send_email
# def send_email(receiver_email, subject, message):
#     try:
#         # Construct the email content
#         text = f"Subject: {subject}\n\n{message}"

#         # Connect to the SMTP server
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()

#             # Login to the SMTP server
#             server.login('jeevanchoudhary2421@gmail.com', 'sdyo knaw zkgj kvkd ')

#             # Send the email
#             server.sendmail('jeevanchoudhary2421@gmail.com', receiver_email, text)
#             print('Email sent successfully.')

#     except Exception as e:
#         print('Failed to send email:', e)

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
            if current_user.public_id == "None":
                current_user.public_id=str(uuid.uuid4())
                db.session.commit()
                return make_response(jsonify({'message': 'Token is invalid!'}), 401)
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
            return make_response(jsonify({'message': 'Please enter all fields!', 'status': 'error'}), 400)
        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response(jsonify({'message': 'User does not exist!', 'status': 'error'}), 404)
        if check_password_hash(user.password, password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow(
            ) + timedelta(minutes=30)}, DevelopmentConfig.SECRET_KEY, algorithm="HS256")

            if user.role != 'admin':
                email = Profile.query.filter_by(profile_id=user.profile_id).first().email
                print(email)
                subject = "Login Succeed"
                body = render_template('mail_login.html',customer_name=Profile.query.filter_by(profile_id=user.profile_id).first().firstname,token=user.public_id)

                # Start a new thread to send the email
                thread = threading.Thread(target=send_email, args=(email, subject, body))
                thread.start()

                user.active = True
                db.session.commit()



            return make_response(jsonify({'token': token, 'user_data': user.serialize(), 'status': 'success'}), 200)
        return make_response(jsonify({'message': 'Incorrect password!', 'status': 'error'}), 401)

api.add_resource(Login, '/login')



class Dashboard(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, current_user):
        print(current_user)
        # send_email(Profile.query.filter_by(profile_id=current_user.profile_id).first().email, "Login", "You have Logged in")

        # email = Profile.query.filter_by(profile_id=current_user.profile_id).first().email
        # print(email)
        # subject = "Login"
        # body = "You have Logged in"

        # # Start a new thread to send the email
        # thread = threading.Thread(target=send_email, args=(email, subject, body))
        # thread.start()

        # send_email(Profile.query.filter_by(profile_id=current_user.profile_id).first().email, "Monthly Report", "monthly_report_template")
        # msg_title = "Monthly Report"
        # sender = 'noreply@librarymanagementsystem.com'
        # msg = Message(msg_title, sender=sender, recipients=[Profile.query.filter_by(profile_id=current_user.profile_id).first().email])
        # mail.send(msg)


        res = redis_client.get('dashboard')
        print(Profile.query.filter_by(profile_id=current_user.profile_id).first().email)
        if not res:
            if current_user.role == 'admin':
                return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
            books = Books.query.all()
            books = books[::-1] 
            books_lst=[]
            for book in books:
                temp = book.serialize()
                temp["date_issue"] = book.date_issue.strftime("%Y-%m-%d %H:%M:%S")
                books_lst.append(temp)

            books_lst_section = []
            sections = Section.query.all()
            for section in sections:
                books=Books.query.filter_by(section_id=section.section_id).all()
                books = books[::-1] 
                if len(books)==0:
                    continue
                books_temp=[]
                for book in books:
                    temp = book.serialize()
                    temp['section_name'] = section.section_name
                    temp["date_issue"] = book.date_issue.strftime("%Y-%m-%d %H:%M:%S")
                    books_temp.append(temp)
                books_lst_section.append(books_temp)
            print(current_user.serialize())
            dashboard = {'message': 'Welcome to the dashboard!',
                                      'books': books_lst,
                                      'books_lst_section':books_lst_section,
                                      'status': 'success'}
            redis_client.set("dashboard", json.dumps(dashboard))
            redis_client.expire("dashboard", timedelta(hours=6))
            dashboard['user_data'] = current_user.serialize()
        else:
            dashboard = json.loads(res)
            dashboard['user_data'] = current_user.serialize()
            if dashboard['user_data']['role'] == "admin":
                return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)

        dashboard['user_data'] = current_user.serialize()
        return make_response(jsonify(dashboard), 200)

api.add_resource(Dashboard, '/dashboard')

class Search(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, current_user, search):
        books = Books.query.filter(Books.book_name.ilike('%'+search+'%')).all()
        books_lst=[]
        for book in books:
            temp = book.serialize()
            temp["section_name"]=Section.query.filter_by(section_id=book.section_id).first().section_name
            temp["date_issue"] = book.date_issue.strftime("%Y-%m-%d %H:%M:%S")
            books_lst.append(temp)
        return make_response(jsonify({'books': books_lst, 'status': 'success','user_data': current_user.serialize()}), 200)

api.add_resource(Search, '/search/<string:search>')

class VerifyUser(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, current_user):
        return make_response(jsonify({'message': 'Authorized', 'status': 'success'}), 200)

api.add_resource(VerifyUser, '/verify_user')

class adminDashboard(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, current_user):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        section = Section.query.all()
        section_lst=[]
        for sec in section:
            section_temp=[]
            section_temp.append(sec.serialize())
            books_temp = []
            books = Books.query.filter_by(section_id=sec.section_id).all()
            books = books[::-1] 
            for book in books:
                books_temp.append(book.serialize())
            temp=[section_temp,books_temp]
            section_lst.append(temp)
        return make_response(jsonify({'message': 'Welcome to the admin\'s dashboard!','user_data': current_user.serialize(),'section': section_lst, 'status': 'success'}), 200)

                
api.add_resource(adminDashboard, '/admin_dashboard')

class Book(Resource):
    method_decorators = {'get': [token_required]}
    def get(self,current_user,book_id):
        if current_user.role == 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
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

class AdminBook(Resource):
    method_decorators = {'get': [token_required]}
    def get(self,current_user,book_id):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
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

api.add_resource(AdminBook, '/adminbook/<int:book_id>')



class fetchbookimg(Resource):
    def get(self, book_id):
        book = Books.query.filter_by(book_id=book_id).first()
        if book:
            return Response(book.image, mimetype="image/jpeg")
        return make_response(jsonify({'message': 'Book not found!', 'status': 'error'}), 404)
    
api.add_resource(fetchbookimg, '/fetchbookimg/<int:book_id>')


# class AddBooks(Resource):
    
#     def post(self):
        
#         data = request.json
#         if len(data['description'].split())>300 or sum(c.isalpha() for c in data['description']) >1600:
#             return make_response(jsonify({'message': 'Description should not exceed 300 words or 1600 characters', 'status': 'error'}), 400)
#         try:
#             date_issue = datetime.now()
#             book = Books(book_name=data['book_name'], author=data['author'], image=data['image'], section_id=data['section_id'],date_issue=date_issue, status=data['status'], description=data['description'], title=data['title'])
#             db.session.add(book)
#             db.session.commit()
#             return make_response(jsonify({'message': 'Book added successfully', 'status': 'success'}), 201)
#         except Exception as e:
#             db.session.rollback()
#             return make_response(jsonify({'error': str(e)}), 500)
        
# api.add_resource(AddBooks, '/add_books')

class AddBooks(Resource):
    method_decorators = {'post': [token_required]}
    def post(self, current_user):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        if request.files:
            # Handle file upload
            image_file = request.files['image']
            image_data = image_file.read()

            try:
                if 'pdf_file' not in request.files:
                    return 'No file part'
                
                file = request.files['pdf_file']
                print(file)
                
                if file.filename == '':
                    return make_response(jsonify({'message': 'No selected file', 'status': 'error'}), 400)
                
                if file:
                    filename = file.filename+str(random.randint(1,1000000))
                    print("filename",filename)
                    file.save(os.path.join("pdfuploads", filename))
                    path=os.path.join("pdfuploads", filename)
                    print(path)
                    # print file path
                    print("file saved")
                    book_id=random.randint(1,1000000)
                    new_pdf = PDF(filename=filename,book_id=book_id,path=path)
                    print(new_pdf)
                    db.session.add(new_pdf)
                    db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify({'error': str(e)}), 500)

            # Handle form data
            try:
                date_issue = datetime.now()
                book_data = request.form
                print(book_data)
                book = Books(
                    book_id=book_id,
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
                redis_client.delete('adminsummary')
                redis_client.delete('dashboard')
                return make_response(jsonify({'message': 'Book added successfully', 'status': 'success'}), 201)
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(AddBooks, '/add_books')

class EditBook(Resource):
    method_decorators = {'post': [token_required]}
    def post(self, current_user):
        print(request.files)
        print('image' in request.files)
        print('pdf_file' in request.files)
        print(request.form)

        try:
            if request.form['book_id'] == "" or request.form['book_name'] == "" or request.form['author'] == "" or request.form['section_id'] == "" or request.form['status'] == "" or request.form['description'] == "" or request.form['title'] == "":
                return make_response(jsonify({'message': 'All fields are required', 'status': 'error'}), 400)
            if len(request.form['description'].split())>300 and sum(c.isalpha() for c in request.form['description']) >2600:
                return make_response(jsonify({'message': 'Description should not exceed 300 words or 2600 characters', 'status': 'error'}), 400)
            
            book=Books.query.filter_by(book_id=request.form['book_id']).first()
            book.book_name = request.form['book_name']
            book.author = request.form['author']
            book.section_id = request.form['section_id']
            book.status = request.form['status']
            book.description = request.form['description']
            book.title = request.form['title']

            if 'image' in request.files:
                image_file = request.files['image']
                image_data = image_file.read()
                book.image = image_data

            if 'pdf_file' in request.files:
                file = request.files['pdf_file']
                print(file)
                if file.filename == '':
                    return make_response(jsonify({'message': 'No selected file', 'status': 'error'}), 400)
                if file:
                    try:
                        if PDF.query.filter_by(book_id=book.book_id).first():
                            pdf = PDF.query.filter_by(book_id=book.book_id).first()
                            filename = pdf.filename
                            file.save(os.path.join("pdfuploads", filename))
                            path=os.path.join("pdfuploads", filename)
                            print(path)
                            # print file path
                            print("file saved")
                            pdf.path=path
                            db.session.commit()
                        else:
                            filename = file.filename+str(random.randint(1,1000000))
                            print("filename",filename)
                            file.save(os.path.join("pdfuploads", filename))
                            path=os.path.join("pdfuploads", filename)
                            print(path)
                            # print file path
                            print("file saved")
                            new_pdf = PDF(filename=filename,book_id=request.form['book_id'],path=path)
                            print(new_pdf)
                            db.session.add(new_pdf)
                            db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        return make_response(jsonify({'error': str(e)}), 500)
            db.session.commit()
            redis_client.delete('dashboard')
            redis_client.delete('adminsummary')
            return make_response(jsonify({'message': 'Book edited successfully', 'status': 'success'}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)

    # def post(self, current_user):
    #     if current_user.role != 'admin':
    #         return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        
    #     print(request.files)
    #     if request.files:
    #         # Handle file upload
    #         image_file = request.files['image']
    #         image_data = image_file.read()

    #         try:
    #             if 'pdf_file' not in request.files:
    #                     return make_response(jsonify({'message': 'No file part', 'status': 'error'}), 400)
                    
    #             file = request.files['pdf_file']
    #             print(file)
                
    #             if file.filename == '':
    #                 return make_response(jsonify({'message': 'No selected file', 'status': 'error'}), 400)
                
    #             if file:
    #                 book=Books.query.filter_by(book_id=request.form['book_id']).first()
    #                 pdf = PDF.query.filter_by(book_id=book.book_id).first()
    #                 filename = pdf.filename
    #                 file.save(os.path.join("pdfuploads", filename))
    #                 path=os.path.join("pdfuploads", filename)
    #                 print(path)
    #                 # print file path
    #                 print("file saved")
    #                 new_pdf = PDF(filename=filename,book_id=request.form['book_id'],path=path)
    #                 print(new_pdf)
    #                 db.session.add(new_pdf)
    #                 db.session.commit()
    #                 print("dddd")
    #         except Exception as e:
    #             db.session.rollback()
    #             return make_response(jsonify({'error': str(e)}), 500)

    #         try:
    #             book_data = request.form
    #             book = Books.query.filter_by(book_id=book_data['book_id']).first()
    #             if book_data['book_name'] == "" or book_data['author'] == "" or book_data['section_id'] == "" or book_data['status'] == "" or book_data['description'] == "" or book_data['title'] == "":
    #                 return make_response(jsonify({'message': 'All fields are required', 'status': 'error'}), 400)
    #             if len(book_data['description'].split())>300 and sum(c.isalpha() for c in book_data['description']) >1600:
    #                 return make_response(jsonify({'message': 'Description should not exceed 300 words or 1600 characters', 'status': 'error'}), 400)
    #             # for book in Books.query.all():
    #             #     if book.book_name == book_data['book_name'] and book.book_id != book_data['book_id']:
    #             #         return make_response(jsonify({'message': 'Book already exists', 'status': 'error'}), 409)
    #             book.book_name = book_data['book_name']
    #             book.author = book_data['author']
    #             book.image = image_data
    #             book.section_id = book_data['section_id']
    #             book.status = book_data['status']
    #             book.description = book_data['description']
    #             book.title = book_data['title']
    #             db.session.commit()
    #             redis_client.delete('dashboard')
    #             redis_client.delete('adminsummary')
    #             return make_response(jsonify({'message': 'Book added successfully', 'status': 'success'}), 201)
    #         except Exception as e:
    #             db.session.rollback()
    #             return make_response(jsonify({'error': str(e)}), 500)
    #         # Handle form data
    #     else:
    #         try:
    #             book_data = request.form
    #             book = Books.query.filter_by(book_id=book_data['book_id']).first()
    #             if book_data['book_name'] == "" or book_data['author'] == "" or book_data['section_id'] == "" or book_data['status'] == "" or book_data['description'] == "" or book_data['title'] == "":
    #                 return make_response(jsonify({'message': 'All fields are required', 'status': 'error'}), 400)
    #             if len(book_data['description'].split())>300 and sum(c.isalpha() for c in book_data['description']) >1600:
    #                 return make_response(jsonify({'message': 'Description should not exceed 300 words or 1600 characters', 'status': 'error'}), 400)
    #             # for book in Books.query.all():
    #             #     if book.book_name == book_data['book_name'] and book.book_id != book_data['book_id']:
    #             #         return make_response(jsonify({'message': 'Book already exists', 'status': 'error'}), 409)
    #             book.book_name = book_data['book_name']
    #             book.author = book_data['author']
    #             book.section_id = book_data['section_id']
    #             book.status = book_data['status']
    #             book.description = book_data['description']
    #             book.title = book_data['title']
    #             db.session.commit()
    #             redis_client.delete('dashboard')
    #             redis_client.delete('adminsummary')
    #             return make_response(jsonify({'message': 'Book Edited successfully', 'status': 'success'}), 201)
    #         except Exception as e:
    #             db.session.rollback()
    #             return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(EditBook, '/edit_book')


class AddSection(Resource):
    method_decorators = {'post': [token_required]}

    def post(self, current_user):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        data = request.json
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
            redis_client.delete('dashboard')
            redis_client.delete('adminsummary')
            return make_response(jsonify({'message': 'Section added successfully', 'status': 'success'}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
        
api.add_resource(AddSection, '/add_section')

class EditSection(Resource):
    method_decorators = {'post': [token_required]}

    def post(self, current_user):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        data = request.json
        try:
            section = Section.query.filter_by(section_id=data['section_id']).first()
            if section:
                section.section_name = data['section_name']
                section.description = data['description']
                db.session.commit()
                redis_client.delete('dashboard')
                redis_client.delete('adminsummary')
                return make_response(jsonify({'message': 'Section updated successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Section not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
        
api.add_resource(EditSection, '/edit_section')

class DeleteSection(Resource):
    method_decorators = {'post': [token_required]}

    def post(self, current_user):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        data = request.json
        try:
            section = Section.query.filter_by(section_id=data['section_id']).first()
            if section:
                books = Books.query.filter_by(section_id=data['section_id']).all()
                if books:
                    for book in books:
                        db.session.delete(book)
                db.session.delete(section)
                db.session.commit()
                redis_client.delete('dashboard')
                redis_client.delete('adminsummary')
                return make_response(jsonify({'message': 'Section deleted successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Section not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(DeleteSection, '/delete_section')

class DeleteBook(Resource):
    method_decorators = {'post': [token_required]}

    def post(self, current_user):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        data = request.json
        try:
            book = Books.query.filter_by(book_id=data['book_id']).first()
            if book:
                db.session.delete(book)
                db.session.commit()
                redis_client.delete('dashboard')
                redis_client.delete('adminsummary')
                return make_response(jsonify({'message': 'Book deleted successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Book not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(DeleteBook, '/delete_book')

class RequestBook(Resource):
    method_decorators = {'post': [token_required]}
    
    def post(self, current_user):
        if current_user.role == 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        data = request.json
        try:
            if data['period'] == "":
                return make_response(jsonify({'message': 'All fields are required', 'status': 'error'}), 400)
            if int(data['period']) <= 0:
                return make_response(jsonify({'message': 'Invalid period', 'status': 'error'}), 400)
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
                redis_client.delete('adminsummary')

                return make_response(jsonify({'message': 'Your Request for edit is successful', 'status': 'success'}), 200)
            if Issue.query.filter_by(user_id=current_user.id).count() >= 5:
                return make_response(jsonify({'message': 'You have reached the maximum limit of 5 books', 'status': 'error'}), 400)
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
        if current_user.role == 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        data = request.json
        try:
            issue = Issue.query.filter_by(user_id=current_user.id, book_id=data['book_id'], status='Requested').first()
            if issue:
                db.session.delete(issue)
                db.session.commit()
                redis_client.delete('adminsummary')
                return make_response(jsonify({'message': 'Request cancelled successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Request not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
    
api.add_resource(CancelRequest, '/cancel_request')

class RequestedBooks(Resource):
    method_decorators = {'get': [token_required]}

    def get(self,current_user, status):
        if current_user.role == 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        issues = Issue.query.filter_by(user_id=current_user.id).all()
        issues_lst = []
        books_lst = []
        for issue in issues:
            if issue.status == status:
                issue_temp =[issue.serialize()]
                issue_temp.append(Books.query.filter_by(book_id=issue.book_id).first().short_serialize())
                issues_lst.append(issue_temp)
        redis_client.delete('adminsummary')
        return make_response(jsonify({'requested_books': issues_lst, 'status': 'success', 'current_user': current_user.serialize()}), 200)

api.add_resource(RequestedBooks, '/requested_books/<string:status>')

class ReturnBook(Resource):
    method_decorators = {'post': [token_required]}

    def post(self,current_user):
        if current_user.role == 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        data = request.json
        try:
            issue = Issue.query.filter_by(user_id=current_user.id, book_id=data['book_id'], status='Issued').first()
            if issue:
                db.session.delete(issue)
                history = History(book_id=data['book_id'], user_id=current_user.id, date_issue=issue.date_issue, return_date=datetime.now(),status='Returned',section_id=Books.query.filter_by(book_id=data['book_id']).first().section_id)
                db.session.add(history)
                db.session.commit()
                redis_client.delete('adminsummary')
                return make_response(jsonify({'message': 'Book returned successfully', 'status': 'success'}), 200)
            return make_response(jsonify({'message': 'Book not found', 'status': 'error'}), 404)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(ReturnBook, '/return_book')

class CancelAllRequests(Resource):
    method_decorators = {'post': [token_required]}
    
    def post(self, current_user):
        if current_user.role == 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        try:
            issues = Issue.query.filter_by(user_id=current_user.id, status='Requested').all()
            for issue in issues:
                db.session.delete(issue)
                db.session.commit()
            redis_client.delete('adminsummary')
            return make_response(jsonify({'message': 'All requests cancelled successfully', 'status': 'success'}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
    
api.add_resource(CancelAllRequests, '/cancel_all_requests')

class ReturnAllBooks(Resource):
    method_decorators = {'post': [token_required]}

    def post(self,current_user):
        try:
            if current_user.role == 'admin':
                return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
            issues = Issue.query.filter_by(user_id=current_user.id, status='Issued').all()
            for issue in issues:
                history = History(book_id=issue.book_id, user_id=current_user.id, date_issue=issue.date_issue, return_date=datetime.now(),status='Returned',section_id=Books.query.filter_by(book_id=issue.book_id).first().section_id)
                db.session.delete(issue)
                db.session.add(history)
                db.session.commit()
            redis_client.delete('adminsummary')
            return make_response(jsonify({'message': 'All books returned successfully', 'status': 'success'}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
        
api.add_resource(ReturnAllBooks, '/return_all_books')

class HistoryBooks(Resource):
    method_decorators = {'get': [token_required]}

    def get(self,current_user):
        if current_user.role == 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        history = History.query.filter_by(user_id=current_user.id).all()
        history_lst = []
        for h in history:
            history_lst.append(h.serialize())
        return make_response(jsonify({'history': history_lst, 'status': 'success'}), 200)
    
api.add_resource(HistoryBooks, '/history')

class AdminBookRequested(Resource):
    method_decorators = [token_required]

    def get(self,current_user):
        Issue.refresh()
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        issues = Issue.query.all()
        issues_lst = []
        for issue in issues:
            if issue.status != 'Requested':
                continue
            issue_temp =[issue.serialize()]
            issue_temp.append(Books.query.filter_by(book_id=issue.book_id).first().short_serialize())
            issue_temp.append(User.query.filter_by(id=issue.user_id).first().serialize())
            issue_temp.append(Section.query.filter_by(section_id=Books.query.filter_by(book_id=issue.book_id).first().section_id).first().serialize())
            issue_temp.append(Profile.query.filter_by(profile_id=User.query.filter_by(id=issue.user_id).first().profile_id).first().serialize())
            issues_lst.append(issue_temp)
        return make_response(jsonify({'issues': issues_lst, 'status': 'success','current_user': current_user.serialize()}), 200)
    
api.add_resource(AdminBookRequested, '/adminbookrequested')

class RequestAccept(Resource):
    method_decorators = [token_required]

    def get(self,current_user,book_id):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        issue = Issue.query.filter_by(book_id=book_id, status='Requested').first()
        if issue:
            issue.status = 'Issued'
            db.session.commit()
            redis_client.delete('adminsummary')
            return make_response(jsonify({'message': 'Request accepted successfully', 'status': 'success'}), 200)
        return make_response(jsonify({'message': 'Request not found', 'status': 'error'}), 404)
    
api.add_resource(RequestAccept, '/requestaccept/<int:book_id>')

class RequestReject(Resource):
    method_decorators = [token_required]

    def get(self,current_user,book_id):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        issue = Issue.query.filter_by(book_id=book_id, status='Requested').first()
        if issue:
            history = History(book_id=issue.book_id, user_id=issue.user_id, date_issue=issue.date_issue, return_date=datetime.now(),status='Rejected',section_id=Books.query.filter_by(book_id=issue.book_id).first().section_id)
            db.session.add(history)
            db.session.delete(issue)
            db.session.commit()
            redis_client.delete('adminsummary')
            return make_response(jsonify({'message': 'Request rejected successfully', 'status': 'success'}), 200)
        return make_response(jsonify({'message': 'Request not found', 'status': 'error'}), 404)
    
api.add_resource(RequestReject, '/requestreject/<int:book_id>')

class RevokeAccess(Resource):
    method_decorators = [token_required]

    def get(self,current_user,book_id):
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        issue = Issue.query.filter_by(book_id=book_id, status='Issued').first()
        if issue:
            history = History(book_id=issue.book_id, user_id=issue.user_id, date_issue=issue.date_issue, return_date=datetime.now(),status='Revoked',section_id=Books.query.filter_by(book_id=issue.book_id).first().section_id)
            db.session.add(history)
            db.session.delete(issue)
            db.session.commit()
            redis_client.delete('adminsummary')
            return make_response(jsonify({'message': 'Access revoked successfully', 'status': 'success'}), 200)
        return make_response(jsonify({'message': 'Request not found', 'status': 'error'}), 404)
    
api.add_resource(RevokeAccess, '/revokeaccess/<int:book_id>')

class AdminBookIssued(Resource):
    method_decorators = [token_required]

    def get(self,current_user):
        Issue.refresh()
        if current_user.role != 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        issues = Issue.query.all()
        issues_lst = []
        for issue in issues:
            if issue.status != 'Issued':
                continue
            issue_temp =[issue.serialize()]
            issue_temp.append(Books.query.filter_by(book_id=issue.book_id).first().short_serialize())
            issue_temp.append(User.query.filter_by(id=issue.user_id).first().serialize())
            issue_temp.append(Section.query.filter_by(section_id=Books.query.filter_by(book_id=issue.book_id).first().section_id).first().serialize())
            issue_temp.append(Profile.query.filter_by(profile_id=User.query.filter_by(id=issue.user_id).first().profile_id).first().serialize())
            issues_lst.append(issue_temp)
        return make_response(jsonify({'issues': issues_lst, 'status': 'success','current_user': current_user.serialize()}), 200)

api.add_resource(AdminBookIssued, '/adminbookissued')

class AdminSummary(Resource):
    method_decorators = [token_required]

    def get(self,current_user):
        res = redis_client.get('adminsummary')
        if not res:
            if current_user.role != 'admin':
                return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
            books=Books.query.all()
            books_lst=[]
            books_count=[]
            sections_count=[]
            sections_name=[]
            status_count=[]
            status_name=[]
            for book in books:
                books_lst.append(book.book_name)
                books_count.append(History.query.filter_by(book_id=book.book_id).count())
            for section in Section.query.all():
                sections_name.append(section.section_name)
                sections_count.append(History.query.filter_by(section_id=section.section_id).count())

            for books in History.query.all():
                if books.status in status_name:
                    continue
                status_name.append(History.query.filter_by(status=books.status).first().status)
                status_count.append(History.query.filter_by(status=books.status).count())
            adminsummary = {'books': books_lst, 
                            'books_count': books_count, 
                            'status': 'success',
                            'current_user': current_user.serialize(),
                            'sections_count': sections_count,
                            'sections_name': sections_name,
                            'status_name':status_name,
                            'status_count':status_count}
            
            redis_client.set("adminsummary", json.dumps(adminsummary))
            redis_client.expire("adminsummary", timedelta(hours=6))
        else:
            adminsummary = json.loads(res)
            if adminsummary['current_user']['role'] != current_user.role:
                return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        
        return make_response(jsonify(adminsummary), 200)
api.add_resource(AdminSummary, '/adminsummary')

class UserSummary(Resource):
    method_decorators = [token_required]

    def get(self,current_user):
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
        
        return make_response(jsonify({'books': books_lst, 'books_count': books_count, 'status': 'success','current_user': current_user.serialize(),'sections_count': sections_count,'sections_name': sections_name,'status_name':status_name,'status_count':status_count}), 200)
api.add_resource(UserSummary, '/usersummary')

class BookRead(Resource):
    method_decorators = [token_required]

    def get(self,current_user,book_id):
        if current_user.role == 'admin':
            return make_response(jsonify({'message': 'You are not authorized to access this page!', 'status': 'error'}), 401)
        
        pdf=PDF.query.filter_by(book_id=book_id).first()
        with open(pdf.path, 'rb') as f:
            pdf_data = f.read() 
        # return make_response(pdf_data, 200)
        return send_file(pdf.path, as_attachment=True)

    
api.add_resource(BookRead, '/bookread/<int:book_id>')

class pdfshow(Resource):
    def get(self):
        pdf=PDF.query.filter_by(book_id=10).first()
        with open(pdf.path, 'rb') as f:
            pdf_data = f.read() 
        # return make_response(pdf_data, 200)
        return Response(pdf_data, mimetype="application/pdf")
api.add_resource(pdfshow, '/pdfshow')