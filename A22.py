import pandas as pd
from datetime import datetime
import datetime
import random
import requests
import streamlit as st

df = pd.read_excel("babbel2.xlsx")

title = st.text_input('Norwegian word').lower()


if len(title)>0:
    st.write(f'{title} is in the database file')
    st.write(df[df.NOWEGIAN == title])

genre = st.radio("Is this a new word?",
    ('Yes', 'No'))


