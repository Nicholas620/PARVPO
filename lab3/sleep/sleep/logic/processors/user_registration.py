import json
import pika
from controllers.models.models import User

def process_user_registration(body, session):
    user_data = json.loads(body)
    password_hash = user_data['password']
    user_data['password_hash'] = password_hash
    try:
        new_user = User(
            name=user_data['name'],
            email=user_data['email'],
            password_hash=user_data['password_hash'],
            birth_date=user_data['birth_date']
        )
        session.add(new_user)
        session.commit()
        print(f"User registered: {user_data['email']}")
    except Exception as e:
        print(f"Failed to register user: {e}")
        session.rollback()
