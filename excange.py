import streamlit as st
from currencies.parse import Currency


def convert_currency():
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

    # Converting currencies
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
