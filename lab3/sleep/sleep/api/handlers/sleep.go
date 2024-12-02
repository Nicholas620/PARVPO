package handlers

import (
    "encoding/json"
    "log"
    "sleep-activity/api/models"
    "sleep-activity/api/rabbitmq"
    "sleep-activity/api/utils"
    "net/http"
)

func AddSleepHandler(w http.ResponseWriter, r *http.Request) {
    utils.SetCommonHeaders(w)

    if r.Method == "OPTIONS" {
        return
    }

    if r.Method != http.MethodPost {
        utils.WriteErrorResponse(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var sleepData models.SleepDataRequest
    err := json.NewDecoder(r.Body).Decode(&sleepData)
    if err != nil {
        utils.WriteErrorResponse(w, "Bad request", http.StatusBadRequest)
        return
    }

    log.Printf("Received sleep data: %+v\n", sleepData)

    body, err := json.Marshal(sleepData)
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

    err = rabbitmq.PublishMessage("add_user_sleep", body, correlationID, replyQueue.Name)
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
            var sleepResponse models.SleepDataResponse
            err := json.Unmarshal(msg.Body, &sleepResponse)
            if err != nil {
                utils.WriteErrorResponse(w, "Failed to parse response", http.StatusInternalServerError)
                return
            }

            if sleepResponse.Error != "" {
                log.Printf("Failed to add sleep record: %s\n", sleepResponse.Error)
                utils.WriteErrorResponse(w, sleepResponse.Error, http.StatusBadRequest)
            } else {
                utils.WriteJSONResponse(w, sleepResponse, http.StatusOK)
                log.Printf("Sleep record added successfully for user %s\n", sleepData.Name)
            }
            break
        }
    }
}
