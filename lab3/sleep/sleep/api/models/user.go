package models

type User struct {
    Name      string `json:"name"`
    Email     string `json:"email"`
    Password  string `json:"password"`
    BirthDate string `json:"birth_date"`
}

type UserResponse struct {
    User struct {
        Name      string `json:"name"`
        Email     string `json:"email"`
        BirthDate string `json:"birth_date"`
    } `json:"user"`
    SleepRecords []struct {
        RecordID        int     `json:"record_id"`
        SleepStartTime  string  `json:"sleep_start_time"`
        SleepEndTime    string  `json:"sleep_end_time"`
        QualityScore    float64 `json:"quality_score"`
        TotalAwakeTime  int     `json:"total_awake_time"`
        Duration        int     `json:"duration"`
        GptComments     string  `json:"gpt_comments"`
    } `json:"sleep_records"`
    Error string `json:"error,omitempty"`
}
