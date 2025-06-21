import requests
from logger_config import logger


# main code
class IpChecking:
    def __init__(self):
        self.url = "https://api.2ip.ua/geo.json?ip="
        self.response = None
        self.result = None

    def fetch(self):
        try:
            self.response = requests.get(self.url)
            self.response.raise_for_status()
            self.result = self.response.json()

            logger.info(f"IP info: {self.result}")
            return self.result

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e} (status {self.response.status_code})")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
