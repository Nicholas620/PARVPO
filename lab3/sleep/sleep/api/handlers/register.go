package handlers

import (
    "encoding/json"
    "log"
    "sleep-activity/api/models"
    "sleep-activity/api/rabbitmq"
    "sleep-activity/api/utils"
    "net/http"
)

func RegisterHandler(w http.ResponseWriter, r *http.Request) {
    utils.SetCommonHeaders(w)

    if r.Method == "OPTIONS" {
        return
    }

    if r.Method != http.MethodPost {
        utils.WriteErrorResponse(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var user models.User
    err := json.NewDecoder(r.Body).Decode(&user)
    if err != nil {
        utils.WriteErrorResponse(w, "Bad request", http.StatusBadRequest)
        return
    }

    log.Printf("Received user for registration: %+v\n", user)

    body, err := json.Marshal(user)
    if err != nil {
        utils.WriteErrorResponse(w, "Internal server error", http.StatusInternalServerError)
        return
    }

    err = rabbitmq.PublishMessage("user_registration", body, rabbitmq.GenerateCorrelationID(), "")
    if err != nil {
        utils.WriteErrorResponse(w, "Failed to publish message", http.StatusInternalServerError)
        return
    }

    utils.WriteJSONResponse(w, "User registered successfully", http.StatusOK)
}
