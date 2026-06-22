import os

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

TIMEOUT = 10
RETRY_TOTAL = 3
RETRY_BACKOFF_FACTOR = 1