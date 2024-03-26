from main import app
from models import *

with app.app_context():
    db.create_all()
    db.session.commit()

    print("database created")