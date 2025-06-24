import requests
import streamlit as st
from logger_config import logger


class Currency:
    """Class to work with currencies and amount and rates"""

    @staticmethod
    @st.cache_data(ttl=86400)
    def get_supported_currencies():
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info("Connection to API status: Successful")
                data = response.json()
                rates = {item["cc"]: float(item["rate"]) for item in data}
                return rates
            else:
                error_code = response.json().get("error-type", "unknown")
                logger.error(f"API Error: {error_code}")
                return {}, error_code
        except Exception as e:
            logger.critical(f"Critical error: {e}")
            return {}, str(e)

    def __init__(self):
        self.supported_currencies = self.get_supported_currencies()

    def convert(self, from_curr: str, to_curr: str, amount: float):
        if not self.supported_currencies:
            return None
        if from_curr == to_curr:
            return amount
        if (
            from_curr not in self.supported_currencies
            or to_curr not in self.supported_currencies
        ):
            logger.error("Unsupported currency.")
            return None

        amount_in_uah = amount * self.supported_currencies[from_curr]
        logger.debug(
            f"""Conversion details:
                     From {from_curr}:
                     Amount: {amount},
                     In UAH: {amount_in_uah}"""
        )
        return amount_in_uah / self.supported_currencies[to_curr]
