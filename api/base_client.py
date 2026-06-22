import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.config import BASE_URL, HEADERS, TIMEOUT, RETRY_TOTAL, RETRY_BACKOFF_FACTOR


class BaseClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._attach_retry()

    def _attach_retry(self):
        retry_strategy = Retry(
            total=RETRY_TOTAL,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, endpoint, params=None):
        response = self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response

    def post(self, endpoint, payload=None):
        response = self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response

    def put(self, endpoint, payload=None):
        response = self.session.put(f"{self.base_url}{endpoint}", json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response

    def delete(self, endpoint):
        response = self.session.delete(f"{self.base_url}{endpoint}", timeout=TIMEOUT)
        response.raise_for_status()
        return response