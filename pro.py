import streamlit as st
from urllib.parse import quote_plus
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
import os
import io
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Climate Change",page_icon=":earth_asia:",layout="centered")
st.title(":earth_asia: Green house Gas Emission")
st.markdown('<style>div.block-container{padding-top:lrem;}</style',unsafe_allow_html=True)

df=pd.read_csv("Files\greenhouse-gas-emissions-industry-and-household-december-2023-quarter.csv")

# Initialize session state for the button
if 'show_df' not in st.session_state:
    st.session_state.show_df = False

# Button to toggle the DataFrame display
if st.button('Toggle DataFrame'):
    # Toggle the state
    st.session_state.show_df = not st.session_state.show_df

# Show or hide the DataFrame based on the state
if st.session_state.show_df:
    st.write("Here is the DataFrame:")
    st.write(df)

#Convert DataFrame to CSV string
csv_string = df.to_csv(index=False)
csv_bytes = io.BytesIO(csv_string.encode())
st.download_button(
    label="Download CSV",
    data=csv_bytes,
    file_name='greenhouse-gas-emissions-industry-and-household-december-2023-quarter.csv',
    mime='text/csv'
)   

#Choosing parameter
option = st.selectbox("Select any Parameter",(df["Anzsic_descriptor"].unique()),index=None,placeholder=
                      "Select any parameter for seeing emission of diffrent gases in particular sector:") 
 
category_df = df[df["Anzsic_descriptor"]== option] 

#creating chart
st.subheader(body=option)
fig=px.bar(category_df, x="Period", y="Data_value", color="Gas",text="Gas",orientation="v",hover_name="Gas",
                 color_discrete_sequence=["orange","red","green","yellow", "blue","purple"], 
                 height=500)
fig.update_traces(width=0.7)
fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig.update_xaxes(type='category')
st.plotly_chart(fig, use_container_width=True, height=100,bargap=0.9)

#Choosing gor particular gas
st.subheader(body="Emission of gas over the year")
option1 = st.selectbox("Select specific Gas",df["Gas"].unique(),index=None,placeholder="Gases")
particular_df = category_df[category_df["Gas"]==option1]
# Check if filtered DataFrame is empty
if particular_df.empty:
    st.write(f"No data available for the selected gas: {option1}")
else:
    # Sort by 'Period' to ensure correct plotting
    particular_df = particular_df.sort_values(by='Period')
    
    # Create base line graph
    line = go.Figure()

    # Add main line
    line.add_trace(go.Scatter(x=particular_df['Period'], 
                             y=particular_df['Data_value'],
                             mode='lines',
                             name=f'Emissions of {option1}',
                             line=dict(color='blue')))
    
    # Add the segment connecting the first and last points
    first_point = particular_df.iloc[0]
    last_point = particular_df.iloc[-1]

    line.add_trace(go.Scatter(x=[first_point['Period'], last_point['Period']], 
                             y=[first_point['Data_value'], last_point['Data_value']],
                             mode='lines',
                             name='Start to End',
                             line=dict(color='red', dash='dash')))
    
    # Update layout for better presentation
    line.update_layout(title=f'Emissions of {option1} Over the Years',
                      xaxis_title='Period',
                      yaxis_title='Data_value',
                      legend_title='Legend',
                      height= 500)
    
    # Display the chart
    st.plotly_chart(line, use_container_width=True)
#line = px.line(particular_df, x='Period', y='Data_value', title=f'Emissions of {option1} Over the Years')
#st.plotly_chart(line)

#creating individual chart
st.subheader(body=" % of gas emitted in an individual year")
option2 = st.selectbox("Select specific Year",df["Period"].unique(),index=None,placeholder="Year")

filtered_df = category_df[category_df["Period"]==option2]
cha=px.pie(filtered_df, values="Data_value",names="Gas")
cha.update_traces(marker = dict(line=dict(color='white', width=0.5)))
st.plotly_chart(cha, theme=None)



st.sidebar.header("Learn About")
st.sidebar.markdown("[GreenHouse Gas Emission](https://www.epa.gov/ghgemissions/sources-greenhouse-gas-emissions)")
st.sidebar.markdown("[How do we reduce GreenHouse Gases](https://scied.ucar.edu/learning-zone/climate-solutions/reduce-greenhouse-gases)")
# Sidebar for search input
query = st.sidebar.text_input("Search query:")

# Create Google search URL
if query:
    search_url = f"https://www.google.com/search?q={quote_plus(query)}"
    st.sidebar.markdown(f"[Search Google for '{query}']({search_url})")





   

