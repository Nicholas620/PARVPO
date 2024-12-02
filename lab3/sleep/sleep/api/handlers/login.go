package handlers

import (
    "encoding/json"
    "log"
    "sleep-activity/api/models"
    "sleep-activity/api/rabbitmq"
    "sleep-activity/api/utils"
    "net/http"
)

func LoginHandler(w http.ResponseWriter, r *http.Request) {
    utils.SetCommonHeaders(w)

    if r.Method == "OPTIONS" {
        return
    }

    if r.Method != http.MethodPost {
        utils.WriteErrorResponse(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var loginReq models.LoginRequest
    err := json.NewDecoder(r.Body).Decode(&loginReq)
    if err != nil {
        utils.WriteErrorResponse(w, "Bad request", http.StatusBadRequest)
        return
    }

    log.Printf("Received login request: %+v\n", loginReq)

    body, err := json.Marshal(loginReq)
    if err != nil {
        utils.WriteErrorResponse(w, "Internal server error", http.StatusInternalServerError)
        return
    }

    correlationID := rabbitmq.GenerateCorrelationID()
    replyQueue, err := rabbitmq.Ch.QueueDeclare("", false, true, false, false, nil)
    if err != nil {
        utils.WriteErrorResponse(w, "Failed to declare reply queue", http.StatusInternalServerError)
        return
    }

    err = rabbitmq.PublishMessage("user_login", body, correlationID, replyQueue.Name)
    if err != nil {
        utils.WriteErrorResponse(w, "Failed to publish message", http.StatusInternalServerError)
        return
    }

    msgs, err := rabbitmq.Ch.Consume(replyQueue.Name, "", true, false, false, false, nil)
    if err != nil {
        utils.WriteErrorResponse(w, "Failed to consume from reply queue", http.StatusInternalServerError)
        return
    }

    for msg := range msgs {
        if msg.CorrelationId == correlationID {
            var userResponse models.UserResponse
            err := json.Unmarshal(msg.Body, &userResponse)
            if err != nil {
                utils.WriteErrorResponse(w, "Failed to parse response", http.StatusInternalServerError)
                return
            }

            if userResponse.Error != "" {
                log.Printf("Authentication failed for user %s: %s\n", loginReq.Name, userResponse.Error)
                utils.WriteErrorResponse(w, userResponse.Error, http.StatusUnauthorized)
            } else {
                utils.WriteJSONResponse(w, userResponse, http.StatusOK)
                log.Printf("Authentication successful for user %s\n", loginReq.Name)
            }
            break
        }
    }
}
