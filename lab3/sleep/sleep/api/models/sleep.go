package models

type SleepInfoRequest struct {
    Name string `json:"name"`
}

type SleepDataRequest struct {
    Name            string  `json:"name"`
    SleepStartTime  string  `json:"sleep_start_time"`
    SleepEndTime    string  `json:"sleep_end_time"`
    QualityScore    float64 `json:"quality_score"`
}

type SleepRecord struct {
    RecordID        int     `json:"record_id"`
    SleepStartTime  string  `json:"sleep_start_time"`
    SleepEndTime    string  `json:"sleep_end_time"`
    QualityScore    float64 `json:"quality_score"`
    TotalAwakeTime  int     `json:"total_awake_time"`
    Duration        int     `json:"duration"`
    GptComments     string  `json:"gpt_comments"`
}

type SleepDataResponse struct {
    SleepRecord struct {
        RecordID        int     `json:"record_id"`
        SleepStartTime  string  `json:"sleep_start_time"`
        SleepEndTime    string  `json:"sleep_end_time"`
        QualityScore    float64 `json:"quality_score"`
        TotalAwakeTime  int     `json:"total_awake_time"`
        Duration        int     `json:"duration"`
        GptComments     string  `json:"gpt_comments"`
    } `json:"sleep_record"`
    Error string `json:"error,omitempty"`
}
