const fs = require('fs');
const faker = require('faker');

// Функция для генерации случайных данных пользователей
function generateUsers(numUsers) {
    const users = [];
    for (let i = 0; i < numUsers; i++) {
        const username = faker.internet.userName();
        const email = faker.internet.email();
        const password = faker.internet.password();
        const birthdate = faker.date.past(30, '2000-01-01').toISOString().split('T')[0]; // Пример: 1990-01-01

        users.push({
            username,
            email,
            password,
            birthdate
        });
    }
    return users;
}

// Функция для записи данных в CSV файл
function writeCSV(users) {
    const header = 'username,email,password,birthdate\n';
    const rows = users.map(user => `${user.username},${user.email},${user.password},${user.birthdate}`).join('\n');

    const csvContent = header + rows;

    // Пишем данные в файл
    fs.writeFileSync('./data/users.csv', csvContent, 'utf8');
    console.log('CSV file has been saved!');
}

// Генерируем 10 000 пользователей (можно настроить количество)
const users = generateUsers(10000);
writeCSV(users);
