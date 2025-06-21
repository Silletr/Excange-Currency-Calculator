import requests
from logger_config import logger


# main code
class IpChecking:  # Fixed typo in class name
    def __init__(self):
        self.url = "https://api.2ip.ua/geo.json?ip="
        self.response = None
        self.result = None

    def fetch(self, ip_address):
        try:
            full_url = f"{self.url}{ip_address}"
            self.response = requests.get(full_url)
            self.response.raise_for_status()
            self.data = self.response.json()
            
            logger.info(f"user ip details: {self.data}")
            return self.data
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"http error: {e} (status {self.response.status_code})")
            
        except Exception as e:
            logger.error(f"unexpected error: {e}")
