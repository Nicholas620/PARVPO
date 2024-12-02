package utils

import (
    "net/http"
    "encoding/json"
)

func SetCommonHeaders(w http.ResponseWriter) {
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
    w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
}

func WriteErrorResponse(w http.ResponseWriter, message string, statusCode int) {
    w.WriteHeader(statusCode)
    w.Write([]byte(message))
}

func WriteJSONResponse(w http.ResponseWriter, data interface{}, statusCode int) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(statusCode)
    json.NewEncoder(w).Encode(data)
}
