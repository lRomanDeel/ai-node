# kernel/core/config.py

class Config:
    # --- Retry ---
    MAX_RETRIES = 2              # количество повторов API
    RETRY_BACKOFF = 1.5          # множитель задержки (экспоненциальный)

    # --- Timeout ---
    EXECUTION_TIMEOUT = 300      # общий таймаут задачи (сек)
    API_TIMEOUT = 60             # таймаут HTTP запроса
    LOCAL_TIMEOUT = 600          # локальная модель (может быть дольше)

    # --- Concurrency ---
    MAX_CONCURRENT_TASKS = 2     # ограничение параллелизма (CPU!)

    # --- Input limits ---
    MAX_INPUT_LENGTH = 4000

    # --- Queue ---
    MAX_QUEUE_SIZE = 100
