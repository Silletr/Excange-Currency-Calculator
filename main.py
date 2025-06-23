# Imports
import datetime as dt
import time

import streamlit as st
import streamlit.components.v1 as component

import pytz
from streamlit_js_eval import streamlit_js_eval


from logger_config import logger
from currencies.parse import Currency

# TODO: See detailed tasks below
"""
    1. Add Donate button (at: 08/23/2025)
    2. Optimizate code for better UX
FIXME:
    1. ...
"""
# --------------------------------------------------------------------------------
# Page config and loading dotenv

page_config = st.set_page_config(page_title="Currency Calculator", page_icon="💱")


# -------------------------------------------------------------------
# Tracking time of enter to the site
def enter_time():
    """
    Getting the time when user entered to the site and save to log file
    """
    timezone = pytz.timezone("Europe/Kiev")
    current_datetime = dt.datetime.now(timezone)
    current_datetime = f"{current_datetime.hour:02}:{current_datetime.minute:02}"
    logger.info(f"User entered to the website, time: {current_datetime}")


enter_time()


#  -----------------------------------------------------------------------------------------
# Getting User-Agent of viewer (for separating bots and humans)
def get_user_agent():
    """
    Taking the user agent for separate real user from bot,
    if streamlit_js_eval cant get the user agent on some reasons just returning the "User Agent is unknown"
    """
    logger.info("Waiting for User-Agent")
    time.sleep(2.5)

    # Store directly in session state
    global user_agent
    user_agent = streamlit_js_eval(
        js_expressions="navigator.userAgent", key="getUserAgent"
    )

    if user_agent and isinstance(user_agent, str):
        st.session_state["user_agent"] = user_agent
        logger.debug(f"User Agent: {user_agent}")
    else:
        logger.debug("User-Agent is unknown.")
        st.session_state["user_agent"] = "Unknown"


get_user_agent()
#  -----------------------------------------------------------------------------------------
# Greetings
st.markdown(
    "**Want know how much you need give to the bank for needed amount of currency?** "
    "Calculate this on my Currency-Calculator! Just select amount, two currencies and that's all!"
)
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
if st.button("📜 Show logs"):
    try:
        with open("logs/site_log.log", "r", encoding="utf-8") as f:
            logs = f.read()
        st.text_area("Log file", logs, height=350)

    except FileNotFoundError:
        st.error("Log file not found")
    except Exception as e:
        st.error(f"Error reading log file: {str(e)}")


# -----------------------------------------------------------------------------------------
# Call func with all currencies
def convert_currency():
    """
    converting currency using the Ukrainian National Bank (list of supported currencies: https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json),
    saving result of operation on logs file, and returning result to user on format "amount {from_curr} -> amount {to_curr}"
    """
    # Get currencies and handle potential errors
    result = Currency.get_supported_currencies()

    # Check if we got an error
    if isinstance(result, tuple) and len(result) == 2:
        currencies, error = result
        if error:
            st.warning(
                f"⚠️ Website may not work properly. API error: {error.replace('-', ' ')}"
            )
            return

    currencies = result

    # Fallback to default currencies if none available
    available_currencies = currencies if currencies else ["USD", "UAH", "EUR"]

    # Choosing currency
    from_currency = st.selectbox("From currency", available_currencies)
    to_currency_options = [
        curr for curr in available_currencies if curr != from_currency
    ]
    to_currency = st.selectbox("To currency", to_currency_options)

    # Enter amount
    amount = st.number_input(
        label="Enter amount", step=0.01, max_value=float(1_000_000_000)
    )

    def log_user_agent():
        """
        Log user agent from session state when button is clicked
        """
        # Get user agent from session state
        user_agent = st.session_state.get("user_agent", "Unknown")
        logger.debug(f"User with {user_agent} - real user")

    # Converting currencies
    if st.button("Check amount", on_click=log_user_agent):
        logger.debug(f"User with {user_agent} - real user")
        if "user-agent" not in st.session_state:
            st.session_state["user-agent"] = f"{user_agent}"

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


# -----------------------------------------------------------------------------------------
# Call func with all currencies
convert_currency()
# ------------------------------------------------------------------------------------------

# # Donate (for the future, ~3 month)
# don = Donate()
# don.donate()
