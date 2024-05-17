from main import app
from models import *
from werkzeug.security import generate_password_hash
import uuid

with app.app_context():
    db.create_all()
    db.session.commit()
    try:
        hashed_password = generate_password_hash("admin", method='pbkdf2:sha256')
        profile = Profile(firstname="admin first", lastname="admin last", phone=9876543210, email="admin@admin.com", address="admin address")
        db.session.add(profile)
        db.session.commit()
        user = User(username="admin", password=hashed_password, public_id=str(uuid.uuid4()), active=True, role='admin', profile_id=Profile.query.filter_by(email="admin@admin.com").first().profile_id)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    print("database created")