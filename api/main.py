from flask import Flask
from flask_cors import CORS 
from models import db, User
from config import DevelopmentConfig
from resources import api

# def create_app():
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(DevelopmentConfig)
db.init_app(app)
api.init_app(app)
    # Initialize CORS with desired settings

#     return app

# app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
