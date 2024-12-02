-- Создание таблицы для причин пробуждения
CREATE TABLE IF NOT EXISTS wake_up_reasons (
    reason_id SERIAL PRIMARY KEY,
    reason_description VARCHAR(255) NOT NULL
);

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    birth_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы для записей о сне с новым полем gpt_comments
CREATE TABLE IF NOT EXISTS sleep_records (
    record_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    sleep_start_time TIMESTAMP NOT NULL,
    sleep_end_time TIMESTAMP NOT NULL,
    quality_score FLOAT,
    total_awake_time INTEGER,
    duration INTEGER,
    gpt_comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы пробуждений
CREATE TABLE IF NOT EXISTS wake_ups (
    wake_up_id SERIAL PRIMARY KEY,
    record_id INTEGER REFERENCES sleep_records(record_id) ON DELETE CASCADE,
    wake_up_time TIMESTAMP NOT NULL,
    reason_id INTEGER REFERENCES wake_up_reasons(reason_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
