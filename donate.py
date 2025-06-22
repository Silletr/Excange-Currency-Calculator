import streamlit as st


class Donate:
""" Creating donate button with link to donate service """
    def __init__(self):
        self.donate_link = """
        <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'>
            </script><script type='text/javascript'>
                kofiwidget2.init('Ko-fi', '#3eb6d1', 'Y8Y51GUQWK');kofiwidget2.draw();</script>
        """

    def donate(self):
        if st.button("Send donate: "):
            st.markdown(self.donate_link)
