import json
from datetime import datetime
import time
import os
from pika import BlockingConnection, ConnectionParameters, exceptions
from openai import OpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, SleepRecord
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv('GPT_URL'),
    api_key=os.getenv('OPENAI_API_KEY')
)

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

def connect_to_rabbitmq():
    while True:
        try:
            connection = BlockingConnection(ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), port=os.getenv('RABBITMQ_PORT')))
            channel = connection.channel()

            print("Connected to RabbitMQ successfully.")
            return channel
        except exceptions.AMQPConnectionError:
            print("RabbitMQ not available yet, retrying...")
            time.sleep(5)

def get_gpt_response(prompt, model='gpt-4o'):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты — эксперт по анализу качества сна. Твоя задача — оценивать предоставленные данные о сне и давать рекомендации."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        print(response)

        if response and response.choices:
            return response.choices[0].message.content
        else:
            return "Не удалось получить ответ от модели."
    except Exception as e:
        print(f"Ошибка при обращении к GPT API: {e}")
        return "Произошла ошибка при получении ответа."

def process_generate_gpt_comment(ch, method, properties, body):
    task_data = json.loads(body)
    record_id = task_data.get('record_id')

    session = Session()
    try:
        sleep_record = session.query(SleepRecord).filter_by(record_id=record_id).first()
        if sleep_record:
            user = session.query(User).filter_by(user_id=sleep_record.user_id).first()

            prompt = (
                f"Пользователь: {user.name}\n"
                f"Начало сна: {sleep_record.sleep_start_time.strftime('%Y-%m-%d %H:%M')}\n"
                f"Конец сна: {sleep_record.sleep_end_time.strftime('%Y-%m-%d %H:%M')}\n"
                f"Оценка качества сна: {sleep_record.quality_score}\n"
                f"Продолжительность сна: {sleep_record.duration} минут\n"
                f"Общее время бодрствования: {sleep_record.total_awake_time} минут\n\n"
                f"На основе этих данных, как ты оцениваешь качество сна пользователя и какие рекомендации можешь дать?"
            )

            gpt_response = get_gpt_response(prompt)

            sleep_record.gpt_comments = gpt_response
            session.commit()
            print(f"Комментарий для записи {record_id} успешно сгенерирован.")
        else:
            print(f"Запись о сне с record_id {record_id} не найдена.")
    except Exception as e:
        print(f"Ошибка при генерации комментария для записи {record_id}: {e}")
    finally:
        session.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    channel = connect_to_rabbitmq()
    channel.queue_declare(queue='generate_gpt_comment', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='generate_gpt_comment', on_message_callback=process_generate_gpt_comment)

    print("Воркер запущен и ожидает задач на генерацию комментариев...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
