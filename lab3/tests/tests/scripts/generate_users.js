// scripts/generate_users.js

const fs = require('fs');
const faker = require('faker');

const userCount = 1000; // Количество пользователей для генерации
const users = [];

for (let i = 0; i < userCount; i++) {
  const user = {
    username: faker.internet.userName() + i,
    email: faker.internet.email(),
    password: faker.internet.password(),
    birthdate: faker.date.past(30, new Date(2000, 0, 1)).toISOString().split('T')[0]
  };
  users.push(user);
}

fs.writeFileSync('data/users.json', JSON.stringify(users, null, 2));
console.log(`Сгенерировано ${userCount} пользователей в data/users.json`);
