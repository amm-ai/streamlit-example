from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from deta import Deta


def main_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("Data entry ❄️")
    # Data to be written to Deta Base
    with st.form("form"):
        name = st.text_input("Your name")
        age = st.number_input("Your age")
        submitted = st.form_submit_button("Store in database")


    # Connect to Deta Base with your Project Key
    deta = Deta(st.secrets["deta_key"])

    # Create a new database "example-db"
    # If you need a new database, just use another name.
    db = deta.Base("example-db")

    # If the user clicked the submit button,
    # write the data from the form to the database.
    # You can store any data you want here. Just modify that dictionary below (the entries between the {}).
    if submitted:
        db.put({"name": name, "age": age})

    "---"
    "Here's everything stored in the database:"
    # This reads all items from the database and displays them to your app.
    # db_content is a list of dictionaries. You can do everything you want with it.
    db_content = db.fetch().items
    st.write(db_content)

def page3():
    st.markdown("About 🎉")
    st.sidebar.markdown("ABout 🎉")

page_names_to_funcs = {
    "Main Page": main_page,
    "Data entry": page2,
    "About": page3,
}



def check_password():
    """Returns `True` if the user had a correct password."""
   

   
   
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            
    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    
    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()

