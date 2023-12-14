import streamlit as st
from page.predict_page import show_predict_page
from page.explore_page import show_explore_page


page = st.sidebar.selectbox('Explore Or Predict', ('Predict', 'Explore'))

if page == 'Predict':
    show_predict_page()
else:
    show_explore_page()
