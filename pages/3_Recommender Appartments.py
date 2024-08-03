import streamlit as st
import pandas as pd
import pickle

# Set the page configuration
st.set_page_config(page_title='Recommend Apartments')

# Load the data
location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
location_df_normalized = pickle.load(open('datasets/location_df_normalized.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))


# Define the recommendation function
def recommend_properties_with_scores(property_name, top_n=247):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })
    return recommendations_df


# App title
st.title('Recommend Apartments')

# Section for selecting location and radius
st.header('Select Location and Radius')
selected_location = st.selectbox('Location', sorted(location_df.columns.to_list()))
radius = st.number_input('Radius in Kms', min_value=0.0, step=0.1)

# Initialize a session state for search results
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Search button functionality
if st.button('Search'):
    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
    st.session_state.search_results = result_ser.index.tolist()

    if not st.session_state.search_results:
        st.warning('No property in the given location and radius')
    else:
        st.success(f"Properties within {radius} kms of {selected_location}:")
        for key, value in result_ser.items():
            st.markdown(f"**{key}** --> {round(value / 1000, 2)} kms")

# Section for recommending apartments
st.header('Recommend Apartments')

if st.session_state.search_results:
    selected_apartment = st.selectbox('Select an Apartment', st.session_state.search_results)

    if st.button('Recommend'):
        recommend_df = recommend_properties_with_scores(selected_apartment)
        st.success(f"Top recommended properties similar to **{selected_apartment}**:")
        st.dataframe(recommend_df[['PropertyName', 'SimilarityScore']].head(10))
else:
    st.warning("Please perform a search to select an apartment for recommendations.")

# To make the dataframe display more beautiful
st.markdown("""
<style>
    .css-1d391kg { 
        display: none; 
    }
    .css-1aumxhk {
        font-family: 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)
