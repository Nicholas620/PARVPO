package main

import (
    "log"
    "sleep-activity/api/handlers"
    "sleep-activity/api/rabbitmq"
    "net/http"
)

func main() {
    rabbitmq.ConnectRabbitMQ()

    http.HandleFunc("/health", handlers.HealthCheckHandler)
    http.HandleFunc("/add_sleep", handlers.AddSleepHandler)
    http.HandleFunc("/login", handlers.LoginHandler)
    http.HandleFunc("/register", handlers.RegisterHandler)
    http.HandleFunc("/sleep_info", handlers.SleepInfoHandler)

    log.Println("API server running on port 8080...")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
