import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

def get_session():
    while True:
        try:
            user = os.getenv('POSTGRES_USER')
            password = os.getenv('POSTGRES_PASSWORD')
            host = os.getenv('POSTGRES_HOST')
            port = os.getenv('POSTGRES_PORT')
            db = os.getenv('POSTGRES_DB')

            connection_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
            engine = create_engine(connection_url)
            Session = sessionmaker(bind=engine)
            session = Session()
            print("Connected to PostgreSQL successfully.")
            return session
        except Exception as e:
            print(f"Failed to connect to PostgreSQL: {e}")
            time.sleep(5)
