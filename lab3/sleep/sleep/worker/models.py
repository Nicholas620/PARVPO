from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://application:Armavir@postgres:5432/application"
db = SQLAlchemy(app)


# Таблица пользователей
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)  # Пароль в зашифрованном виде
    birth_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с записями о сне
    sleep_records = db.relationship('SleepRecord', backref='user', lazy=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'birth_date': self.birth_date.strftime('%Y-%m-%d'),  # Форматируем дату в строку
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


# Таблица с записями о сне
class SleepRecord(db.Model):
    __tablename__ = 'sleep_records'
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sleep_start_time = db.Column(db.DateTime, nullable=False)
    sleep_end_time = db.Column(db.DateTime, nullable=False)
    quality_score = db.Column(db.Float)  # Оценка качества сна
    total_awake_time = db.Column(db.Integer)  # Время бодрствования в минутах
    duration = db.Column(db.Integer)  # Длительность сна в минутах
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gpt_comments = db.Column(db.Text)

    # Связь с пробуждениями
    wake_ups = db.relationship('WakeUp', backref='sleep_record', lazy=True)

    def to_dict(self):
        return {
            'record_id': self.record_id,
            'user_id': self.user_id,
            'sleep_start_time': self.sleep_start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'sleep_end_time': self.sleep_end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'quality_score': self.quality_score,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'gpt_comments': self.gpt_comments
        }


class WakeUp(db.Model):
    __tablename__ = 'wake_ups'
    wake_up_id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('sleep_records.record_id'), nullable=False)
    wake_up_time = db.Column(db.DateTime, nullable=False)  # Время пробуждения
    reason_id = db.Column(db.Integer, db.ForeignKey('wake_up_reasons.reason_id'), nullable=False)  # Причина пробуждения
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'wake_up_id': self.wake_up_id,
            'record_id': self.record_id,
            'wake_up_time': self.wake_up_time.strftime('%Y-%m-%d %H:%M:%S'),
            'reason_id': self.reason_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


def calculate_sleep_quality(sleep_record):
    total_wake_time = sum([wake_up.wake_up_time - sleep_record.sleep_start_time for wake_up in sleep_record.wake_ups])

    wake_up_scores = {
        'Шум': 0.2,
        'Болезнь': 0.8,
        'Тревожные мысли': 0.6,
        'Пробуждение по будильнику': 0.1,
        'Неправильная поза': 0.3,
        'Перегрев': 0.4,
        'Другое': 0.5,
    }

    total_score = 0
    for wake_up in sleep_record.wake_ups:
        reason_description = wake_up.reason.reason_description
        total_score += wake_up_scores.get(reason_description, 0.5)

    quality_score = 10 - (total_score * 2 + total_wake_time / 60)
    return max(0, quality_score)


class WakeUpReason(db.Model):
    __tablename__ = 'wake_up_reasons'
    reason_id = db.Column(db.Integer, primary_key=True)
    reason_description = db.Column(db.String(255), nullable=False)  # Описание причины

    # Связь с пробуждениями
    wake_ups = db.relationship('WakeUp', backref='reason', lazy=True)

    def to_dict(self):
        return {
            'reason_id': self.reason_id,
            'reason_description': self.reason_description
        }


def create_db():
    with app.app_context():
        db.create_all()
