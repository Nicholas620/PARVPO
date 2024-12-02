// tests/processor.js

const faker = require('faker');

module.exports = {
  process: function (requestParams, context, ee, next) {
    // Генерация времени начала и окончания сна без секунд
    const sleepStartHour = faker.datatype.number({ min: 21, max: 23 });
    const sleepEndHour = faker.datatype.number({ min: 6, max: 8 });

    context.vars.start_time = `${sleepStartHour}:00`;
    context.vars.end_time = `${sleepEndHour}:00`;
    context.vars.sleep_quality = faker.datatype.number({ min: 1, max: 10 });

    return next();
  }
};
