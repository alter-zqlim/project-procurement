import streamlit as st
import pandas as pd
from helper_functions import utility
from helper_functions import llm

st.set_page_config(
    page_title = "Exploring Procurement Data",
    page_icon=":material/shopping_cart:"
)

st.title("Exploring Procurement Data")
st.write(
    "Users can explore procurement data from GeBiz, based on various procuring agencies, from FY2019 to FY2023."
)

# password checkpoint
if not utility.check_password():  
    st.stop()

# function: read GeBiz data file, set index to "agency"
@st.cache_data
def get_GeBIZ_data():
    unsorted_df = pd.read_csv("./data/GovernmentProcurementviaGeBIZ.csv")
    return unsorted_df.set_index("agency")

# read GeBiz data file, set index to "agency", sort by specified columns, construct index with unique values
unsorted_df = get_GeBIZ_data()
df = unsorted_df.sort_values(by = ['agency', 'tender_no', 'supplier_name', 'award_date'])
df_index = df[~df.index.duplicated(keep = 'first')]

# generate a multi-option selector that displays data based on selected agencies  
agencies = st.multiselect(
    "Select agencies",
    list(df_index.index),
    ["Competition and Consumer Commission of Singapore (CCCS)"]
)
if not agencies:
    st.error("Please select at least one agency.")
else:
    data = df.loc[agencies]
    st.write("## Procurement projects", data.sort_index())

# generate a form for user input
form = st.form(key = "form")
form.subheader("What would you like to know about the above GeBiz procurement data from FY2019 to FY2023?")

user_input = form.text_area(
    "Please enter your query below and press Submit", 
    height = 160
)

# on detecting Submit, processes and writes response to user input
if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_input}")
    response = llm.check_query_type(user_input)
    st.write(response)