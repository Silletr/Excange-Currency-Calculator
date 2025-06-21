import requests
from logger_config import logger


# main code
class IpCheking:
    def __init__(self):
        self.url = "https://api.2ip.ua/geo.json?ip="
        self.response = None
        self.result = None

    def fetch(self):
        try:
            self.response = requests.get(self.url)
            self.response.raise_for_status()
            self.result = self.response.json()
            self.data = self.response.json()
            self.result = self.data.get("ip")

            logger.info(f"user ip: {self.data}")
            return self.result

        except requests.exceptions.httperror as e:
            logger.error(f"http error: {e} (status {self.response.status_code})")

        except Exception as e:
            logger.error(f"unexpected error: {e}")
