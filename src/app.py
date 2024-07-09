import streamlit as st
import sklearn
import pickle

st.title("MSCI 436 - Group 3")

st.header("Features")

with open('../ML Models/linear_regression_model.pkl', 'rb') as file:
    model = pickle.load(file)

row1col1, row1col2, row1col3 = st.columns(3)

with row1col1:
   quarter_of_the_year = st.selectbox("Quarter of the Year", ("Q1", "Q2", "Q3", "Q4"), index=None, placeholder="")

with row1col2:
   origin_province = st.selectbox("Origin Province", ("Q1", "Q2", "Q3", "Q4"), index=None, placeholder="")

with row1col3:
   destination_province = st.selectbox("Destination Province", ("Q1", "Q2", "Q3", "Q4"), index=None, placeholder="")


row2col1, row2col2, row2col3 = st.columns(3)

with row2col1:
   duration_of_the_trip = st.number_input(f'Duration of the Trip (days)', min_value=int(0), max_value=int(334), step=1, value=None)

with row2col2:
   main_reason_of_the_trip = st.selectbox("Main Reason of the Trip", ("Q1", "Q2", "Q3", "Q4"), index=None, placeholder="")

with row2col3:
   main_mode_of_tranportation = st.selectbox("Main Mode of Transportation", ("Q1", "Q2", "Q3", "Q4"), index=None, placeholder="")


row3col1, row3col2 = st.columns(2)

with row3col1:
   number_of_adults = st.slider("Number of Additional Adults", 0, 5, 1)

with row3col2:
   number_of_children = st.slider("Number of Children", 0, 4, 1)

activities_options = ['Visit Friends & Family', 'Shopping', 'Sightseeing', 'Museum/Art Gallery', 'Historic site', 'Zoo/Aquarium', 'Sprts Event as Spectator', 'Festival or Fair', 'Performance such as Play or Concert', 'Casino', 'Theme/Amusement Park', 'Aboriginal Event', 'Movies', 'Restaurant/Bar/Club', 'Wildife Viewing/Bird Watching', 'National/Provincial/Nature Park', 'Medical/Health Treatment', 'Business Meeting/Conference/Seminar', 'All-Terrain Vehicle', 'Boating', 'Canoeing/Kayaking', 'Camping', 'Hiking/Backpacking', 'Fishing', 'Beach', 'Hunting', 'Golfing', 'Cycling', 'Snowmobiling', 'Downhill Skiing/Snowboarding', 'Cross-country Skiing/Snowshoeing', 'Play Sports', 'Other Activity', 'No Activities']
activities = st.multiselect("Activities", activities_options, [])


st.header(model.predict([[], []]))