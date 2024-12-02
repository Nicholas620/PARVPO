package handlers

import (
    "sleep-activity/api/utils"
    "net/http"
)

func HealthCheckHandler(w http.ResponseWriter, r *http.Request) {
    utils.WriteJSONResponse(w, "OK", http.StatusOK)
}
