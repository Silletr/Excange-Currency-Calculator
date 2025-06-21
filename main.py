# Imports
import datetime as dt
import os
import time

import dotenv
import streamlit as st
import streamlit.components.v1 as component
import pytz
from streamlit_js_eval import streamlit_js_eval

from logger_config import logger
from currencies.parse import Currency
# --------------------------------------------------------------------------------
# Page config and loading dotenv

page_config = st.set_page_config(page_title="Currency Calculator", page_icon="💱")
dotenv.load_dotenv()


# -------------------------------------------------------------------
# Tracking time of enter to the site
def enter_time():
    timezone = pytz.timezone("Europe/Kiev")
    current_datetime = dt.datetime.now(timezone)
    current_datetime = f"{current_datetime.hour:02}:{current_datetime.minute:02}"
    logger.info(f"User entered to the website, time: {current_datetime}")


enter_time()
#  -----------------------------------------------------------------------------------------
# Getting User-Agent of viewer (for separating bots and humans)
# Using best method - if stremalit cant give UA (User Agent) - just replacing it to "User-Agent is missing"


def User_Agent():
    # Taking user agent
    logger.warning("Waiting for User-Agent")
    time.sleep(1.5)
    user_agent = streamlit_js_eval(
        js_expressions="navigator.userAgent", key="getUserAgent"
    )

    if user_agent and isinstance(user_agent, str):
        st.session_state["user_agent"] = user_agent
        logger.debug(f"User Agent: {user_agent}")
    else:
        logger.debug("User-Agent is missing. Maybe it`s a Bot.")


User_Agent()
#  -----------------------------------------------------------------------------------------
# Greetings
st.markdown(
    "**Want know how much you need give to the bank for needed amount of currency?** "
    "Calculate this on my Currency-Calculator! Just select amount, two currencies and that's all!"
)

"""
My website dont working until 9th June, because my API quota was ended, 
sorry for thats, and i`ll be wait you right here at designated date!
"""

#  -----------------------------------------------------------------------------------------
# Main functional
component.html(
    """
    <script async src="//gc.zgo.at/count.js"
        data-goatcounter="https://silletr.goatcounter.com/count"
        data-goatcounter-settings='{"clicks": true, "allow_frame": true}'>
    </script>
    """,
    height=0,
)


#  -----------------------------------------------------------------------------------------
# getting IP to check owner for access to log-file
def ip_get():
    ip = streamlit_js_eval(
        js_expressions="""await (async () => {
            try {
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();
                return data.ip || "127.0.0.1";
            } catch (e) {
                return "127.0.0.1";
            }
        })()""",
        key="get-ip",
    )

    return ip


# -----------------------------------------------------------------------------------------
def check_ip(ip):
    if ip:
        owner_ip = os.getenv("OWNER_IP")
        if ip == owner_ip:
            st.success("Hi, Silletr! Logs is done: ")
            if st.button("📜 Show logs"):
                with open("logs/site_log.log", "r", encoding="utf-8") as f:
                    logs = f.read()
                st.text_area("Log file", logs, height=350)
        else:
            logger.info(f"User with IP {ip} is not owner. Access denied.")
    else:
        logger.error("Can't get user IP (it's null or empty).")


user_ip = ip_get()

check_ip(user_ip)


# -----------------------------------------------------------------------------------------
# Call func with all currencies
def convert_currency():
    currencies, error = Currency.get_supported_currencies()

    if error:
        st.warning(
            f"⚠️ Website may not work properly. API error: {error.replace('-', ' ')}"
        )
    # currencies
    available_currencies = currencies if currencies else ["USD", "UAH", "RUB"]
    # Choising currency
    from_currency = st.selectbox("From currency", available_currencies)
    to_currency_options = [
        curr for curr in available_currencies if curr != from_currency
    ]
    to_currency = st.selectbox("To currency", to_currency_options)

    # Enter amount
    amount = st.number_input(
        label="Enter amount", step=0.01, max_value=float(1_000_000_000)
    )

    # Conversting currecies
    if st.button("Check amount"):
        currency = Currency()
        clean_amount = abs(amount)
        result = currency.convert(
            to_curr=to_currency, from_curr=from_currency, amount=clean_amount
        )
        if result is not None:
            st.markdown(
                f"### 💰 {clean_amount} {from_currency} = **{result:.2f} {to_currency}**"
            )

        else:
            st.error("Conversion failed.")


convert_currency()
