import streamlit as st
import sklearn
import pandas as pd
import pickle

# Import Models
with open('../ML Models/model.pkl', 'rb') as file:
    model = pickle.load(file)
with open('../ML Models/modelt.pkl', 'rb') as file:
    modelt = pickle.load(file)
with open('../ML Models/modelfb.pkl', 'rb') as file:
    modelfb = pickle.load(file)
with open('../ML Models/modelat.pkl', 'rb') as file:
    modelat = pickle.load(file)
with open('../ML Models/models.pkl', 'rb') as file:
    models = pickle.load(file)
with open('../ML Models/modelacc.pkl', 'rb') as file:
    modelacc = pickle.load(file)

st.title("Data Powered Vacation Planning")
st.subheader("MSCI 436 - Group 3")

st.markdown("Planning your dream vacation just got easier! This tool provides you with an estimated cost for your trip based on the features you input. Enter details about your destination, number of people, time of year, and planned activities, and let our tool do the rest. Get a quick and accurate estimate to help you budget and plan your perfect getaway. Start planning with confidence today!")

st.subheader("Inputs")

row1col1, row1col2, row1col3 = st.columns(3)

with row1col1:
   quarter_map = {"January - March" : "Quarter_1st Quarter", "April - June" : "Quarter_2nd Quarter", "July - September" : "Quarter_3rd Quarter", "October - December" : "Quarter_4th Quarter"}
   quarter_of_the_year = st.selectbox("Quarter of the Year", (quarter_map.keys()), index=None, placeholder="")

with row1col2:
   origin_province = st.selectbox("Origin Province", ('Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan'), index=None, placeholder="")

with row1col3:
   destination_region = st.selectbox("Destination Region", ('Calgary Area', 'Central Alberta', 'Central Saskatchewan', 'Eastern Ontario', 'Edmonton Area', 'GTA', 'Hamilton-Niagara', 'Montreal Region', 'New Brunswick', 'Newfoundland', 'North Alberta', 'North Manitoba', 'North Saskatchewan', 'North of Toronto', 'Northern BC', 'Northern Ontario', 'Nova Scotia', 'Other Areas', 'Prince Edward Island', 'Quebec City to Saguenay', 'Regina', 'Rocky Mountains', 'Saskatoon', 'South Alberta', 'South Manitoba', 'South Ontario', 'South Saskatchewan', 'Territories', 'Thompson-Okanagan', 'Vancouver Region', 'Western Quebec'), index=None, placeholder="")


row2col1, row2col2, row2col3 = st.columns(3)

with row2col1:
   duration_of_the_trip = st.number_input(f'Duration of the Trip (days)', min_value=int(0), max_value=int(334), step=1, value=None)

with row2col2:
   main_reason_of_the_trip = st.selectbox("Main Reason of the Trip", ('Friends/Relatives', 'Holiday/Leisure/Recreation', 'Shopping'), index=None, placeholder="")

with row2col3:
   main_mode_of_transportation = st.selectbox("Main Mode of Transportation", ('Bus', 'Car', 'Commercial Airline', 'Commercial Boat or Cruise', 'Ferry', 'Train', 'Other', 'Unknown'), index=None, placeholder="")


row3col1, row3col2 = st.columns(2)

with row3col1:
   number_of_adults = st.slider("Number of Additional Adults", 0, 5, 0)

with row3col2:
   number_of_children = st.slider("Number of Children", 0, 4, 0)

activities_options = ['Visit Friends & Family', 'Shopping', 'Sightseeing', 'Museum/Art Gallery', 'Historic site', 'Zoo/Aquarium', 'Sprts Event as Spectator', 'Festival or Fair', 'Performance such as Play or Concert', 'Casino', 'Theme/Amusement Park', 'Aboriginal Event', 'Movies', 'Restaurant/Bar/Club', 'Wildife Viewing/Bird Watching', 'National/Provincial/Nature Park', 'Medical/Health Treatment', 'Business Meeting/Conference/Seminar', 'All-Terrain Vehicle', 'Boating', 'Canoeing/Kayaking', 'Camping', 'Hiking/Backpacking', 'Fishing', 'Beach', 'Hunting', 'Golfing', 'Cycling', 'Snowmobiling', 'Downhill Skiing/Snowboarding', 'Cross-country Skiing/Snowshoeing', 'Play Sports', 'Other Activity', 'No Activities']
activities = st.multiselect("Activities", activities_options, [])

st.divider()

# Check if all fields are filled 
button_status = all([
    quarter_of_the_year,
    origin_province,
    destination_region,
    duration_of_the_trip,
    main_reason_of_the_trip,
    main_mode_of_transportation,
    activities
])
submit = st.button("Calculate", type="primary", disabled= not button_status)

# Activates when the button is pressed
if submit:

   input_data = {
      "DURATION": duration_of_the_trip,
      "GNCQ06A": number_of_adults,
      "GNCQ06B": number_of_children,
      "Main Reason": main_reason_of_the_trip,
      "Main Transportation Method": main_mode_of_transportation,
      "Origin Province": origin_province,
      "New Regions": destination_region   
   }

   for activity in activities:
      input_data[activity] = 1

   # The columns that need one-hot encoding
   one_hot_columns = ["Main Reason", "Main Transportation Method", "Origin Destination New Region"]

   # The feature names as used during model training
   feature_names = ['DURATION', 'GNCQ06A', 'GNCQ06B', 'Origin Destination New Region_AlbertaCalgary Area', 'Origin Destination New Region_AlbertaCentral Alberta', 'Origin Destination New Region_AlbertaCentral Saskatchewan', 'Origin Destination New Region_AlbertaEastern Ontario', 'Origin Destination New Region_AlbertaEdmonton Area', 'Origin Destination New Region_AlbertaGTA', 'Origin Destination New Region_AlbertaHamilton-Niagara', 'Origin Destination New Region_AlbertaMontreal Region', 'Origin Destination New Region_AlbertaNew Brunswick', 'Origin Destination New Region_AlbertaNewfoundland', 'Origin Destination New Region_AlbertaNorth Alberta', 'Origin Destination New Region_AlbertaNorth Manitoba', 'Origin Destination New Region_AlbertaNorth Saskatchewan', 'Origin Destination New Region_AlbertaNorth of Toronto', 'Origin Destination New Region_AlbertaNorthern BC', 'Origin Destination New Region_AlbertaNorthern Ontario', 'Origin Destination New Region_AlbertaNova Scotia', 'Origin Destination New Region_AlbertaOther Areas', 'Origin Destination New Region_AlbertaPrince Edward Island', 'Origin Destination New Region_AlbertaQuebec City to Saguenay', 'Origin Destination New Region_AlbertaRegina', 'Origin Destination New Region_AlbertaRocky Mountains', 'Origin Destination New Region_AlbertaSaskatoon', 'Origin Destination New Region_AlbertaSouth Alberta', 'Origin Destination New Region_AlbertaSouth Manitoba', 'Origin Destination New Region_AlbertaSouth Ontario', 'Origin Destination New Region_AlbertaSouth Saskatchewan', 'Origin Destination New Region_AlbertaTerritories', 'Origin Destination New Region_AlbertaThompson-Okanagan', 'Origin Destination New Region_AlbertaVancouver Region', 'Origin Destination New Region_AlbertaWestern Quebec', 'Origin Destination New Region_British ColumbiaAtlantic Quebec', 'Origin Destination New Region_British ColumbiaCalgary Area', 'Origin Destination New Region_British ColumbiaCentral Alberta', 'Origin Destination New Region_British ColumbiaCentral Saskatchewan', 'Origin Destination New Region_British ColumbiaEastern Ontario', 'Origin Destination New Region_British ColumbiaEdmonton Area', 'Origin Destination New Region_British ColumbiaGTA', 'Origin Destination New Region_British ColumbiaHamilton-Niagara', 'Origin Destination New Region_British ColumbiaMontreal Region', 'Origin Destination New Region_British ColumbiaNew Brunswick', 'Origin Destination New Region_British ColumbiaNewfoundland', 'Origin Destination New Region_British ColumbiaNorth Alberta', 'Origin Destination New Region_British ColumbiaNorth Manitoba', 'Origin Destination New Region_British ColumbiaNorth Saskatchewan', 'Origin Destination New Region_British ColumbiaNorth of Toronto', 'Origin Destination New Region_British ColumbiaNorthern BC', 'Origin Destination New Region_British ColumbiaNorthern Ontario', 'Origin Destination New Region_British ColumbiaNova Scotia', 'Origin Destination New Region_British ColumbiaOther Areas', 'Origin Destination New Region_British ColumbiaPrince Edward Island', 'Origin Destination New Region_British ColumbiaQuebec City to Saguenay', 'Origin Destination New Region_British ColumbiaRegina', 'Origin Destination New Region_British ColumbiaRocky Mountains', 'Origin Destination New Region_British ColumbiaSaskatoon', 'Origin Destination New Region_British ColumbiaSouth Alberta', 'Origin Destination New Region_British ColumbiaSouth East Quebec', 'Origin Destination New Region_British ColumbiaSouth Manitoba', 'Origin Destination New Region_British ColumbiaSouth Ontario', 'Origin Destination New Region_British ColumbiaSouth Saskatchewan', 'Origin Destination New Region_British ColumbiaTerritories', 'Origin Destination New Region_British ColumbiaThompson-Okanagan', 'Origin Destination New Region_British ColumbiaVancouver Region', 'Origin Destination New Region_British ColumbiaWestern Quebec', 'Origin Destination New Region_ManitobaCalgary Area', 'Origin Destination New Region_ManitobaCentral Alberta', 'Origin Destination New Region_ManitobaCentral Saskatchewan', 'Origin Destination New Region_ManitobaEastern Ontario', 'Origin Destination New Region_ManitobaEdmonton Area', 'Origin Destination New Region_ManitobaGTA', 'Origin Destination New Region_ManitobaHamilton-Niagara', 'Origin Destination New Region_ManitobaMontreal Region', 'Origin Destination New Region_ManitobaNew Brunswick', 'Origin Destination New Region_ManitobaNewfoundland', 'Origin Destination New Region_ManitobaNorth Alberta', 'Origin Destination New Region_ManitobaNorth Manitoba', 'Origin Destination New Region_ManitobaNorth Saskatchewan', 'Origin Destination New Region_ManitobaNorth of Toronto', 'Origin Destination New Region_ManitobaNorthern BC', 'Origin Destination New Region_ManitobaNorthern Ontario', 'Origin Destination New Region_ManitobaNova Scotia', 'Origin Destination New Region_ManitobaOther Areas', 'Origin Destination New Region_ManitobaPrince Edward Island', 'Origin Destination New Region_ManitobaQuebec City to Saguenay', 'Origin Destination New Region_ManitobaRegina', 'Origin Destination New Region_ManitobaRocky Mountains', 'Origin Destination New Region_ManitobaSaskatoon', 'Origin Destination New Region_ManitobaSouth Alberta', 'Origin Destination New Region_ManitobaSouth East Quebec', 'Origin Destination New Region_ManitobaSouth Manitoba', 'Origin Destination New Region_ManitobaSouth Ontario', 'Origin Destination New Region_ManitobaSouth Saskatchewan', 'Origin Destination New Region_ManitobaThompson-Okanagan', 'Origin Destination New Region_ManitobaVancouver Region', 'Origin Destination New Region_ManitobaWestern Quebec', 'Origin Destination New Region_New BrunswickAtlantic Quebec', 'Origin Destination New Region_New BrunswickCalgary Area', 'Origin Destination New Region_New BrunswickEastern Ontario', 'Origin Destination New Region_New BrunswickEdmonton Area', 'Origin Destination New Region_New BrunswickGTA', 'Origin Destination New Region_New BrunswickHamilton-Niagara', 'Origin Destination New Region_New BrunswickMontreal Region', 'Origin Destination New Region_New BrunswickNew Brunswick', 'Origin Destination New Region_New BrunswickNewfoundland', 'Origin Destination New Region_New BrunswickNorth Alberta', 'Origin Destination New Region_New BrunswickNorth of Toronto', 'Origin Destination New Region_New BrunswickNorthern BC', 'Origin Destination New Region_New BrunswickNorthern Ontario', 'Origin Destination New Region_New BrunswickNova Scotia', 'Origin Destination New Region_New BrunswickOther Areas', 'Origin Destination New Region_New BrunswickPrince Edward Island', 'Origin Destination New Region_New BrunswickQuebec City to Saguenay', 'Origin Destination New Region_New BrunswickRegina', 'Origin Destination New Region_New BrunswickRocky Mountains', 'Origin Destination New Region_New BrunswickSaskatoon', 'Origin Destination New Region_New BrunswickSouth East Quebec', 'Origin Destination New Region_New BrunswickSouth Ontario', 'Origin Destination New Region_New BrunswickTerritories', 'Origin Destination New Region_New BrunswickThompson-Okanagan', 'Origin Destination New Region_New BrunswickVancouver Region', 'Origin Destination New Region_New BrunswickWestern Quebec', 'Origin Destination New Region_Newfoundland and LabradorAtlantic Quebec', 'Origin Destination New Region_Newfoundland and LabradorCalgary Area', 'Origin Destination New Region_Newfoundland and LabradorCentral Alberta', 'Origin Destination New Region_Newfoundland and LabradorEastern Ontario', 'Origin Destination New Region_Newfoundland and LabradorEdmonton Area', 'Origin Destination New Region_Newfoundland and LabradorGTA', 'Origin Destination New Region_Newfoundland and LabradorHamilton-Niagara', 'Origin Destination New Region_Newfoundland and LabradorLabrador', 'Origin Destination New Region_Newfoundland and LabradorMontreal Region', 'Origin Destination New Region_Newfoundland and LabradorNew Brunswick', 'Origin Destination New Region_Newfoundland and LabradorNewfoundland', 'Origin Destination New Region_Newfoundland and LabradorNorth Alberta', 'Origin Destination New Region_Newfoundland and LabradorNorth of Toronto', 'Origin Destination New Region_Newfoundland and LabradorNorthern Quebec', 'Origin Destination New Region_Newfoundland and LabradorNova Scotia', 'Origin Destination New Region_Newfoundland and LabradorOther Areas', 'Origin Destination New Region_Newfoundland and LabradorPrince Edward Island', 'Origin Destination New Region_Newfoundland and LabradorQuebec City to Saguenay', 'Origin Destination New Region_Newfoundland and LabradorRegina', 'Origin Destination New Region_Newfoundland and LabradorSouth Ontario', 'Origin Destination New Region_Newfoundland and LabradorTerritories', 'Origin Destination New Region_Newfoundland and LabradorThompson-Okanagan', 'Origin Destination New Region_Newfoundland and LabradorVancouver Region', 'Origin Destination New Region_Newfoundland and LabradorWestern Quebec', 'Origin Destination New Region_Nova ScotiaAtlantic Quebec', 'Origin Destination New Region_Nova ScotiaCalgary Area', 'Origin Destination New Region_Nova ScotiaCentral Saskatchewan', 'Origin Destination New Region_Nova ScotiaEastern Ontario', 'Origin Destination New Region_Nova ScotiaEdmonton Area', 'Origin Destination New Region_Nova ScotiaGTA', 'Origin Destination New Region_Nova ScotiaHamilton-Niagara', 'Origin Destination New Region_Nova ScotiaMontreal Region', 'Origin Destination New Region_Nova ScotiaNew Brunswick', 'Origin Destination New Region_Nova ScotiaNewfoundland', 'Origin Destination New Region_Nova ScotiaNorth Alberta', 'Origin Destination New Region_Nova ScotiaNorth Manitoba', 'Origin Destination New Region_Nova ScotiaNorth of Toronto', 'Origin Destination New Region_Nova ScotiaNorthern Ontario', 'Origin Destination New Region_Nova ScotiaNova Scotia', 'Origin Destination New Region_Nova ScotiaOther Areas', 'Origin Destination New Region_Nova ScotiaPrince Edward Island', 'Origin Destination New Region_Nova ScotiaQuebec City to Saguenay', 'Origin Destination New Region_Nova ScotiaRegina', 'Origin Destination New Region_Nova ScotiaRocky Mountains', 'Origin Destination New Region_Nova ScotiaSaskatoon', 'Origin Destination New Region_Nova ScotiaSouth Alberta', 'Origin Destination New Region_Nova ScotiaSouth East Quebec', 'Origin Destination New Region_Nova ScotiaSouth Ontario', 'Origin Destination New Region_Nova ScotiaTerritories', 'Origin Destination New Region_Nova ScotiaVancouver Region', 'Origin Destination New Region_Nova ScotiaWestern Quebec', 'Origin Destination New Region_OntarioAtlantic Quebec', 'Origin Destination New Region_OntarioCalgary Area', 'Origin Destination New Region_OntarioCentral Alberta', 'Origin Destination New Region_OntarioCentral Saskatchewan', 'Origin Destination New Region_OntarioEastern Ontario', 'Origin Destination New Region_OntarioEdmonton Area', 'Origin Destination New Region_OntarioGTA', 'Origin Destination New Region_OntarioHamilton-Niagara', 'Origin Destination New Region_OntarioMontreal Region', 'Origin Destination New Region_OntarioNew Brunswick', 'Origin Destination New Region_OntarioNewfoundland', 'Origin Destination New Region_OntarioNorth Alberta', 'Origin Destination New Region_OntarioNorth Manitoba', 'Origin Destination New Region_OntarioNorth of Toronto', 'Origin Destination New Region_OntarioNorthern BC', 'Origin Destination New Region_OntarioNorthern Ontario', 'Origin Destination New Region_OntarioNova Scotia', 'Origin Destination New Region_OntarioOther Areas', 'Origin Destination New Region_OntarioPrince Edward Island', 'Origin Destination New Region_OntarioQuebec City to Saguenay', 'Origin Destination New Region_OntarioRegina', 'Origin Destination New Region_OntarioRocky Mountains', 'Origin Destination New Region_OntarioSaskatoon', 'Origin Destination New Region_OntarioSouth Alberta', 'Origin Destination New Region_OntarioSouth East Quebec', 'Origin Destination New Region_OntarioSouth Manitoba', 'Origin Destination New Region_OntarioSouth Ontario', 'Origin Destination New Region_OntarioSouth Saskatchewan', 'Origin Destination New Region_OntarioTerritories', 'Origin Destination New Region_OntarioThompson-Okanagan', 'Origin Destination New Region_OntarioTrois-Rivieres Region', 'Origin Destination New Region_OntarioVancouver Region', 'Origin Destination New Region_OntarioWestern Quebec', 'Origin Destination New Region_Prince Edward IslandAtlantic Quebec', 'Origin Destination New Region_Prince Edward IslandCalgary Area', 'Origin Destination New Region_Prince Edward IslandCentral Alberta', 'Origin Destination New Region_Prince Edward IslandEastern Ontario', 'Origin Destination New Region_Prince Edward IslandEdmonton Area', 'Origin Destination New Region_Prince Edward IslandGTA', 'Origin Destination New Region_Prince Edward IslandHamilton-Niagara', 'Origin Destination New Region_Prince Edward IslandMontreal Region', 'Origin Destination New Region_Prince Edward IslandNew Brunswick', 'Origin Destination New Region_Prince Edward IslandNewfoundland', 'Origin Destination New Region_Prince Edward IslandNorth Alberta', 'Origin Destination New Region_Prince Edward IslandNorth Manitoba', 'Origin Destination New Region_Prince Edward IslandNorth of Toronto', 'Origin Destination New Region_Prince Edward IslandNova Scotia', 'Origin Destination New Region_Prince Edward IslandOther Areas', 'Origin Destination New Region_Prince Edward IslandPrince Edward Island', 'Origin Destination New Region_Prince Edward IslandQuebec City to Saguenay', 'Origin Destination New Region_Prince Edward IslandSouth Alberta', 'Origin Destination New Region_Prince Edward IslandSouth East Quebec', 'Origin Destination New Region_Prince Edward IslandSouth Ontario', 'Origin Destination New Region_Prince Edward IslandThompson-Okanagan', 'Origin Destination New Region_Prince Edward IslandVancouver Region', 'Origin Destination New Region_Prince Edward IslandWestern Quebec', 'Origin Destination New Region_QuebecAtlantic Quebec', 'Origin Destination New Region_QuebecCalgary Area', 'Origin Destination New Region_QuebecEastern Ontario', 'Origin Destination New Region_QuebecEdmonton Area', 'Origin Destination New Region_QuebecGTA', 'Origin Destination New Region_QuebecHamilton-Niagara', 'Origin Destination New Region_QuebecMontreal Region', 'Origin Destination New Region_QuebecNew Brunswick', 'Origin Destination New Region_QuebecNewfoundland', 'Origin Destination New Region_QuebecNorth Alberta', 'Origin Destination New Region_QuebecNorth Manitoba', 'Origin Destination New Region_QuebecNorth of Toronto', 'Origin Destination New Region_QuebecNorthern BC', 'Origin Destination New Region_QuebecNorthern Ontario', 'Origin Destination New Region_QuebecNorthern Quebec', 'Origin Destination New Region_QuebecNova Scotia', 'Origin Destination New Region_QuebecOther Areas', 'Origin Destination New Region_QuebecPrince Edward Island', 'Origin Destination New Region_QuebecQuebec City to Saguenay', 'Origin Destination New Region_QuebecRocky Mountains', 'Origin Destination New Region_QuebecSouth East Quebec', 'Origin Destination New Region_QuebecSouth Ontario', 'Origin Destination New Region_QuebecSouth Saskatchewan', 'Origin Destination New Region_QuebecTerritories', 'Origin Destination New Region_QuebecThompson-Okanagan', 'Origin Destination New Region_QuebecTrois-Rivieres Region', 'Origin Destination New Region_QuebecVancouver Region', 'Origin Destination New Region_QuebecWestern Quebec', 'Origin Destination New Region_SaskatchewanCalgary Area', 'Origin Destination New Region_SaskatchewanCentral Alberta', 'Origin Destination New Region_SaskatchewanCentral Saskatchewan', 'Origin Destination New Region_SaskatchewanEastern Ontario', 'Origin Destination New Region_SaskatchewanEdmonton Area', 'Origin Destination New Region_SaskatchewanGTA', 'Origin Destination New Region_SaskatchewanHamilton-Niagara', 'Origin Destination New Region_SaskatchewanMontreal Region', 'Origin Destination New Region_SaskatchewanNew Brunswick', 'Origin Destination New Region_SaskatchewanNewfoundland', 'Origin Destination New Region_SaskatchewanNorth Alberta', 'Origin Destination New Region_SaskatchewanNorth Manitoba', 'Origin Destination New Region_SaskatchewanNorth Saskatchewan', 'Origin Destination New Region_SaskatchewanNorth of Toronto', 'Origin Destination New Region_SaskatchewanNorthern BC', 'Origin Destination New Region_SaskatchewanNorthern Ontario', 'Origin Destination New Region_SaskatchewanNova Scotia', 'Origin Destination New Region_SaskatchewanOther Areas', 'Origin Destination New Region_SaskatchewanPrince Edward Island', 'Origin Destination New Region_SaskatchewanQuebec City to Saguenay', 'Origin Destination New Region_SaskatchewanRegina', 'Origin Destination New Region_SaskatchewanRocky Mountains', 'Origin Destination New Region_SaskatchewanSaskatoon', 'Origin Destination New Region_SaskatchewanSouth Alberta', 'Origin Destination New Region_SaskatchewanSouth East Quebec', 'Origin Destination New Region_SaskatchewanSouth Manitoba', 'Origin Destination New Region_SaskatchewanSouth Ontario', 'Origin Destination New Region_SaskatchewanSouth Saskatchewan', 'Origin Destination New Region_SaskatchewanTerritories', 'Origin Destination New Region_SaskatchewanThompson-Okanagan', 'Origin Destination New Region_SaskatchewanVancouver Region', 'Origin Destination New Region_SaskatchewanWestern Quebec', 'Main Transportation Method_Bus', 'Main Transportation Method_Car', 'Main Transportation Method_Commercial Airline', 'Main Transportation Method_Commercial Boat or Cruise', 'Main Transportation Method_Ferry', 'Main Transportation Method_Other', 'Main Transportation Method_Train', 'Main Transportation Method_Unknown', 'Quarter_1st Quarter', 'Quarter_2nd Quarter', 'Quarter_3rd Quarter', 'Quarter_4th Quarter', 'Main Reason_Friends/Relatives', 'Main Reason_Holiday/Leisure/Recreation', 'Main Reason_Shopping', 'Visit Friends & Family', 'Restaurant/Bar/Club', 'Shopping', 'Sightseeing', 'Museum/Art Gallery', 'Historic site', 'Zoo/Aquarium', 'Wildife Viewing/Bird Watching', 'National/Provincial/Nature Park']

   input_data['Origin Destination New Region'] = input_data['Origin Province'] + input_data['New Regions']
   
   input_df = pd.DataFrame([input_data])

   # Perform one-hot encoding on input data
   input_df = pd.get_dummies(input_df, columns=one_hot_columns)

   # Set default values for each column 
   for col in feature_names:
      if col not in input_df.columns:
         input_df[col] = 0
      if col == quarter_map[quarter_of_the_year]:
         input_df[col] = 1

   input_df = input_df[feature_names]
   
   total_cost = model.predict(input_df)[0][0]
   transport_cost = modelt.predict(input_df)[0][0]
   foodbev_cost = modelfb.predict(input_df)[0][0]
   activities_cost = modelat.predict(input_df)[0][0]
   shopping_cost = models.predict(input_df)[0][0]
   accomodation_cost = modelacc.predict(input_df)[0][0]

   st.markdown(f'## Estimated Total Cost: ${max(total_cost, 0):.2f}')
   st.markdown(f'### Estimated Transport Cost: ${max(transport_cost, 0):.2f}')
   st.markdown(f'### Estimated Food & Beverage Cost: ${max(foodbev_cost, 0):.2f}')
   st.markdown(f'### Estimated Activities Cost: ${max(activities_cost, 0):.2f}')
   st.markdown(f'### Estimated Shopping Cost: ${max(shopping_cost, 0):.2f}')
   st.markdown(f'### Estimated Accomodation Cost: ${max(accomodation_cost, 0):.2f}')