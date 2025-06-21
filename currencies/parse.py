import os

import requests
from dotenv import load_dotenv
import streamlit as st

from logger_config import logger

load_dotenv()

API_KEY = os.getenv("API_KEY")


class Currency:
    def __init__(self):
        self.api_key = API_KEY
        self.supported_currencies = self.get_supported_currencies()

    @staticmethod
    @st.cache_data(ttl=86400)
    def get_supported_currencies():
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        try:
            # Connecting to the API
            response = requests.get(url).json()
            if response.get("result") == "success":
                logger.info("Connection to API status: Succefull")
                return list(response["conversion_rates"].keys()), None

            elif response.get("result") == "error":
                error_code = response.get("error-type")
                logger.error(f"Critical error: {error_code}.")
                return [], error_code

        except Exception as e:
            logger.critical(f"Critical error: {e}")
            return [], str(e)

    def convert(self, from_curr: int, to_curr: int, amount: int):
        if self.response("result") == "error" and (
            self.response.get("error-type") == "quota-reached"
        ):
            st.error("""Quota of API requests reached, 
                     try again 09.07.2025. Sorry!""")

        # swap currencies if they are selected in two selectboxes
        if (
            from_curr not in self.supported_currencies
            or to_curr not in self.supported_currencies
        ):
            logger.info("One of the currencies is not supported.")
            return None

        # convert currency
        url = (
            "https://v6.exchangerate-api.com/v6/"
            + "{self.api_key}/pair/{from_curr}/{to_curr}/{amount}"
        )
        # getting json results with rates and currencies
        response = requests.get(url).json()
        if response["result"] == "success":
            # Calculating the rate
            logger.debug(
                f"""Amount money from {from_curr} to {to_curr}: 
                    {amount} {to_curr}"""
            )
            return response["conversion_result"]
        else:
            logger.critical(f"Critical error: {response}")

            print("Conversion failed:", response)
            return None
