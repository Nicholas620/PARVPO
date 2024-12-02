import json
from datetime import datetime
from controllers.models.models import User, SleepRecord
import pika

def process_add_sleep(body, session, ch, properties):
    sleep_data = json.loads(body)
    name = sleep_data.get('name')
    sleep_start_time = sleep_data.get('sleep_start_time')
    sleep_end_time = sleep_data.get('sleep_end_time')
    quality_score = sleep_data.get('quality_score')

    response = {}
    error_message = ""

    try:
        user = session.query(User).filter(User.name == name).first()

        if user is None:
            error_message = "Пользователь не найден"
        else:
            sleep_start = datetime.strptime(sleep_start_time, "%Y-%m-%dT%H:%M")
            sleep_end = datetime.strptime(sleep_end_time, "%Y-%m-%dT%H:%M")
            duration_seconds = (sleep_end - sleep_start).total_seconds()
            duration_minutes = int(duration_seconds // 60)

            total_awake_time = 0

            new_sleep_record = SleepRecord(
                user_id=user.user_id,
                sleep_start_time=sleep_start,
                sleep_end_time=sleep_end,
                quality_score=quality_score,
                duration=duration_minutes,
                total_awake_time=total_awake_time,
                gpt_comments="Комментарий обрабатывается..."
            )
            session.add(new_sleep_record)
            session.commit()

            comment_task = {
                "record_id": new_sleep_record.record_id
            }

            ch.basic_publish(
                exchange='',
                routing_key='generate_gpt_comment',
                body=json.dumps(comment_task),
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )

            response = {
                "sleep_record": {
                    "record_id": new_sleep_record.record_id,
                    "sleep_start_time": sleep_start_time,
                    "sleep_end_time": sleep_end_time,
                    "quality_score": quality_score,
                    "duration": duration_minutes,
                    "total_awake_time": total_awake_time,
                    "gpt_comments": new_sleep_record.gpt_comments
                }
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
