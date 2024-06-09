import streamlit as st
import pandas as pd 


st.title("MSCI 436 - Project")

st.header("Our Data")
df = pd.read_csv("Trips_data.csv")
st.dataframe(df)

st.header("UI Examples")
st.subheader("Example: Multiselect Input")
options = st.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"])

st.write("You selected:", options)

st.subheader("Example: Select Input")
options = st.selectbox(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"])

st.write("You selected:", options)

st.subheader("Example: Radio Input")
genre = st.radio(
    "What's your favorite movie genre?",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    index=None,
)

st.write("You selected:", genre)

st.subheader("Example: Number Input")
number = st.number_input(f'Insert a number (min: {0}, max: {100})', min_value=int(0), max_value=int(100), step=1)
st.write("The current number is ", number)


st.subheader("Example: Column Layout")
col1, col2, col3 = st.columns(3)

with col1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg")