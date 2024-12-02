package handlers

import (
    "encoding/json"
    "log"
    "sleep-activity/api/models"
    "sleep-activity/api/rabbitmq"
    "sleep-activity/api/utils"
    "net/http"
)

func SleepInfoHandler(w http.ResponseWriter, r *http.Request) {
    utils.SetCommonHeaders(w)

    if r.Method == "OPTIONS" {
        return
    }

    if r.Method != http.MethodPost {
        utils.WriteErrorResponse(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var sleepInfoReq models.SleepInfoRequest
    err := json.NewDecoder(r.Body).Decode(&sleepInfoReq)
    if err != nil {
        utils.WriteErrorResponse(w, "Bad request", http.StatusBadRequest)
        return
    }

    log.Printf("Received sleep_info request: %+v\n", sleepInfoReq)

    body, err := json.Marshal(sleepInfoReq)
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

    err = rabbitmq.PublishMessage("sleep_info", body, correlationID, replyQueue.Name)
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
            var sleepDataResponse models.UserResponse
            err := json.Unmarshal(msg.Body, &sleepDataResponse)
            if err != nil {
                utils.WriteErrorResponse(w, "Failed to parse response", http.StatusInternalServerError)
                return
            }

            log.Printf("Received response for user %s: %+v\n", sleepInfoReq.Name, sleepDataResponse)

            if sleepDataResponse.Error != "" {
                log.Printf("Error while fetching sleep info for user %s: %s\n", sleepInfoReq.Name, sleepDataResponse.Error)
                utils.WriteErrorResponse(w, sleepDataResponse.Error, http.StatusInternalServerError)
            } else {
                utils.WriteJSONResponse(w, sleepDataResponse, http.StatusOK)
                log.Printf("Successfully fetched sleep info for user %s\n", sleepInfoReq.Name)

                log.Printf("Successfully returned sleep info for user %s\n", sleepInfoReq.Name)
            }
            break
        }
    }
}
