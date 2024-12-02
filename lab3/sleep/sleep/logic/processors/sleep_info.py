import json
from controllers.models.models import User, SleepRecord
import pika

def process_sleep_info(body, session, ch, properties):
    request_data = json.loads(body)
    name = request_data.get('name')

    response = {}
    error_message = ""

    try:
        user = session.query(User).filter(User.name == name).first()

        if user is None:
            error_message = "Пользователь не найден"
        else:
            sleep_records = session.query(SleepRecord).filter(SleepRecord.user_id == user.user_id).all()

            response = {
                "user": {
                    "name": user.name,
                    "email": user.email,
                    "birth_date": str(user.birth_date)
                },
                "sleep_records": [
                    {
                        "record_id": record.record_id,
                        "sleep_start_time": str(record.sleep_start_time),
                        "sleep_end_time": str(record.sleep_end_time),
                        "quality_score": record.quality_score,
                        "total_awake_time": record.total_awake_time,
                        "duration": record.duration,
                        "gpt_comments": record.gpt_comments
                    }
                    for record in sleep_records
                ]
            }
    except Exception as e:
        error_message = f"Ошибка сервера: {e}"
        print(f"Error: {e}")
    finally:
        session.close()

    if error_message:
        response = {"error": error_message}

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=json.dumps(response)
    )
