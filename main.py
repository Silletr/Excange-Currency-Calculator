# Imports
import datetime as dt
import streamlit as st

import pytz
from streamlit_js_eval import streamlit_js_eval
import streamlit.components.v1 as component
from logger_config import logger
from currencies.parse import Currency


# Tasks:
#   1. Add Donate button (at: 08/23/2025)
#   2. Optimizate code for better UX
# Done:
# - [x] Optimizate code for better UX
# --------------------------------------------------------------------------------
# Page config and loading dotenv

page_config = st.set_page_config(page_title="Currency Calculator", page_icon="💱")

#  -----------------------------------------------------------------------------------------
# Greetings
st.markdown(
    "**Want know how much you need give to the bank for needed amount of currency?** "
    "Calculate this on my Currency-Calculator! Just select amount, two currencies and that's all!"
)

component.html(
    """
    <script async src="//gc.zgo.at/count.js"
        data-goatcounter="https://silletr.goatcounter.com/count"
        data-goatcounter-settings='{"clicks": true, "allow_frame": true}'>
    </script>
    """,
    height=0,
)


# -------------------------------------------------------------------
# Tracking time of enter to the site
def enter_time():
    timezone = pytz.timezone("Europe/Kiev")
    current_datetime = dt.datetime.now(timezone)

    current_time_str = f"{current_datetime.hour:02}:{current_datetime.minute:02}"
    logger.info(f"User entered the website at {current_time_str}")


enter_time()


#  -----------------------------------------------------------------------------------------
def get_user_agent():
    if "user_agent" not in st.session_state:
        st.session_state["user_agent"] = streamlit_js_eval(
            js_expressions="navigator.userAgent", key="getUserAgent"
        )
        logger.debug(f"User Agent: {st.session_state['user_agent'] or 'Unknown'}")
    return st.session_state["user_agent"] or "Unknown"


user_agent = get_user_agent()


#  -----------------------------------------------------------------------------------------
# Main functional
#  -----------------------------------------------------------------------------------------
if "show_logs" not in st.session_state:
    st.session_state.show_logs = False


def toggle_logs():
    st.session_state.show_logs = not st.session_state.show_logs


st.button(
    "📜 Show logs" if not st.session_state.show_logs else "📕 Hide logs",
    on_click=toggle_logs,
)

if st.session_state.show_logs:
    try:
        with open("logs/site_log.log", "r", encoding="utf-8") as f:
            logs = f.readlines()
        logs_to_show = "".join(logs[-300:])  # last 300 strings
        st.text_area("Log file (last 300 lines)", logs_to_show, height=350)
    except FileNotFoundError:
        st.error("Log file not found")
    except Exception as e:
        st.error(f"Error reading log file: {e}")


# --------------------------------------------------------------------------------------
# Currency logic
@st.cache_data(ttl=86400)
def get_currency():
    return Currency()


currency = get_currency()
currencies = currency.supported_currencies
available_currencies = list(currencies.keys())

from_curr = st.selectbox("From currency", available_currencies)
to_curr = st.selectbox(
    "To currency", [c for c in available_currencies if c != from_curr]
)
amount = st.number_input("Amount", step=0.01, max_value=1_000_000_000.0)
clean_amount = abs(amount)

if st.button("Convert"):
    logger.debug(f"User {st.session_state['user_agent']} clicked Convert")

    result = currency.convert(from_curr, to_curr, clean_amount)

    if result is not None:
        st.markdown(f"### 💰 {clean_amount} {from_curr} = **{result:.2f} {to_curr}**")
    else:
        st.error("Conversion failed.")
