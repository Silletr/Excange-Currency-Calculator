import requests
import streamlit as st
from logger_config import logger

class Currency:
    def __init__(self):
        self.supported_currencies = self.get_supported_currencies()

    @staticmethod
    @st.cache_data(ttl=86400)
    def get_supported_currencies():
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                logger.info("Connection to API status: Successful")
                data = response.json()
                
                rates = {item['cc']: float(item["rate"]) for item in data}
                return rates
            
            elif response.status_code >= 400:
                error_code = response.get("error-type", "unknown")
                logger.error(f"API Error: {error_code}")
                return {}, error_code

        except Exception as e:
            logger.critical(f"Critical error: {e}")
            return {}, str(e)

    def convert(self, from_curr: str, to_curr: str, amount: int):
        if self.supported_currencies is None:
            st.error("Failed to fetch currency rates!")
            return None

        if from_curr == to_curr:
            return amount

        if from_curr not in self.supported_currencies or to_curr not in self.supported_currencies:
            logger.error("Unsupported currency.")
            return None

        # Convert currency
        amount_in_uah = amount * float(self.supported_currencies[from_curr])
        result = amount_in_uah / float(self.supported_currencies[to_curr])
        
        logger.debug(
            f"""Conversion details:
               From {from_curr}: {amount}
               In UAH: {amount_in_uah}
               Final {to_curr}: {result:.2f}"""
        )
        return result
