import requests
from logger_config import logger

# main code
class IpChecking:
    def __init__(self):
        self.base_url = "https://api.2ip.io/"
        self.logger = logger
        
    def fetch(self, ip_address=None):
        try:
            # If no IP provided, get current visitor's IP
            if not ip_address:
                endpoint = "info"
            else:
                endpoint = f"info?ip={ip_address}"
                
            url = f"{self.base_url}{endpoint}"
            self.logger.debug(f"Making API request to: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            self.logger.info(f"API response received: {json.dumps(data, indent=2)}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise
