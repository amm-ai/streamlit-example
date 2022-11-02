# streamlit_app.py

import streamlit as st
import snowflake.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()



# Data to be written to Deta Base
with st.form("form", clear_on_submit=True):
    n = st.text_input("Your name")
    c = st.text_input("Are you a chicken?")
    submitted = st.form_submit_button("Store in database")
  
if submitted:
    run_query("INSERT INTO CHICKEN_TABLE VALUES ('n','c');")
    data = run_query("SELECT * from CHICKEN_TABLE;")
    # Print results.
    st.write(data)
