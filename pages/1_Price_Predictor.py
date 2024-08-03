import streamlit as st
import pickle
import pandas as pd
import numpy as np
import joblib
import sklearn
from joblib import dump, load

# Set dark theme for Streamlit page
st.set_page_config(page_title='Real Estate Price Prediction', layout='wide', page_icon="🏠")

# Load data and model pipeline
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

# with open('pipeline.pkl', 'rb') as file:
#     pipeline = pickle.load(file)
# # st.success("Pipeline loaded successfully!")

# # Load with joblib
pipeline = load('pipeline.joblib')

# Header and input fields
st.header('Enter Your Inputs')

property_type = st.selectbox('Property Type', ['flat', 'house'])

sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

bedroom = float(st.selectbox('No. of Bedrooms', sorted(df['bedRoom'].unique().tolist())))

bathroom = float(st.selectbox('No. of Bathrooms', sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input('Built-up Area'))

servant_room = st.selectbox('Servant Room', [0.0, 1.0])

store_room = st.selectbox('Store Room', [0.0, 1.0])

furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))

floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

# Prediction button
if st.button('Predict'):
    # Form a DataFrame with user input
    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, built_up_area, servant_room, store_room,
             furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)
    st.dataframe(one_df)

    # Make prediction and calculate price range
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # Display predicted price range
    st.info(f"The estimated price is between {low:.2f} and {high:.2f} crore ")

# Custom CSS to improve visibility in dark theme
