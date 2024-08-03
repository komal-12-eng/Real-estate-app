import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud

# Page configuration
st.set_page_config(page_title='Real Estate Analysis', layout='wide')
st.title('Real Estate Analytical Module')


# Function to generate word cloud
def generate_word_cloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Load datasets
new_df = pd.read_csv('datasets/data_viz1.csv')
wordcloud_df = pd.read_csv('datasets/new_wordcloud_df.csv')
df = pd.read_csv('datasets/gurgaon_properties_missing_value_imputation.csv')

# Mapbox scatter plot
st.header('Price and Built-up Area Map')
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude",
                        color="price_per_sqft", size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        zoom=10, mapbox_style="open-street-map",
                        width=1200, height=700, hover_name=group_df.index)
st.plotly_chart(fig, use_container_width=True)

# Word cloud section
st.header('Word Cloud for Features by Sector')
specific_sector = st.selectbox('Select Sector for Word Cloud', wordcloud_df['sector'].unique(), key='wordcloud_sector')
sector_features = ' '.join(wordcloud_df[wordcloud_df['sector'] == specific_sector]['features'])
generate_word_cloud(sector_features, f'Word Cloud for {specific_sector}')

# Scatter plot section
st.header('Area vs Price Scatter Plot')
df['sector'] = df['sector'].astype(str)
sectors = ['overall'] + df['sector'].unique().tolist()
selected_sector_scatter = st.selectbox('Select Sector for Scatter Plot', sectors, key='scatter_sector')
filtered_df_scatter = df if selected_sector_scatter == 'overall' else df[df['sector'] == selected_sector_scatter]
fig = px.scatter(filtered_df_scatter, x="built_up_area", y="price", color="bedRoom", title=f"Area Vs Price ({selected_sector_scatter})")
st.plotly_chart(fig)

# Pie chart section
st.header('Distribution of Bedrooms')
selected_sector_pie = st.selectbox('Select Sector for Pie Chart', sectors, key='pie_sector')
filtered_df_pie = df if selected_sector_pie == 'overall' else df[df['sector'] == selected_sector_pie]
fig = px.pie(filtered_df_pie, names='bedRoom', title=f'Pie Chart of Bedrooms in {selected_sector_pie}')
st.plotly_chart(fig)

# Boxplot section
st.header('Price Range for Different BHKs')
temp_df = df[df['bedRoom'] <= 4]
selected_sector_boxplot = st.selectbox('Select Sector for Boxplot', sectors, key='boxplot_sector')
filtered_df_boxplot = temp_df if selected_sector_boxplot == 'overall' else temp_df[temp_df['sector'] == selected_sector_boxplot]
fig = px.box(filtered_df_boxplot, x='bedRoom', y='price', title=f'BHK Price Range ({selected_sector_boxplot})')
st.plotly_chart(fig)

# Distribution plots section
st.header('Price Distribution for Houses and Flats')
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
sns.histplot(df[df['property_type'] == 'house']['price'], kde=True, ax=ax[0], color='blue')
ax[0].set_title('Price Distribution for Houses')
sns.histplot(df[df['property_type'] == 'flat']['price'], kde=True, ax=ax[1], color='green')
ax[1].set_title('Price Distribution for Flats')
st.pyplot(fig)

st.write("© 2024 Real Estate Analytical Module. All rights reserved.")
