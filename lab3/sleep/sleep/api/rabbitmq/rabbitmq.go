package rabbitmq

import (
    "log"
    "time"
    "crypto/rand"
    "encoding/hex"
    "github.com/streadway/amqp"
)

var Ch *amqp.Channel
var userQueue, loginQueue amqp.Queue

func ConnectRabbitMQ() {
    var conn *amqp.Connection
    var err error

    for i := 0; i < 10; i++ {
        conn, err = amqp.Dial("amqp://guest:guest@rabbitmq:5672/")
        if err == nil {
            break
        }
        log.Printf("Failed to connect to RabbitMQ, retrying in 5 seconds... (%d/10)", i+1)
        time.Sleep(5 * time.Second)
    }

    if err != nil {
        log.Fatalf("Failed to connect to RabbitMQ after 10 attempts: %s", err)
    }
    log.Println("Connected to RabbitMQ successfully")

    Ch, err = conn.Channel()
    if err != nil {
        log.Fatalf("Failed to open a channel: %s", err)
    }

    userQueue, err = Ch.QueueDeclare(
        "user_registration",
        false,
        false,
        false,
        false,
        nil,
    )
    if err != nil {
        log.Fatalf("Failed to declare user_registration queue: %s", err)
    }

    loginQueue, err = Ch.QueueDeclare(
        "user_info",
        false,
        false,
        false,
        false,
        nil,
    )
    if err != nil {
        log.Fatalf("Failed to declare user_info queue: %s", err)
    }
}

func GenerateCorrelationID() string {
    b := make([]byte, 16)
    rand.Read(b)
    return hex.EncodeToString(b)
}

func PublishMessage(queueName string, body []byte, correlationID, replyTo string) error {
    return Ch.Publish(
        "",
        queueName,
        false,
        false,
        amqp.Publishing{
            ContentType:   "application/json",
            Body:          body,
            ReplyTo:       replyTo,
            CorrelationId: correlationID,
        })
}
