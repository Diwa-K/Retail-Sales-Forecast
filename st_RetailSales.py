# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import pickle

# Setting up page configuration
st.set_page_config(page_title= "Retail sales forecasting",
                   layout= "wide",
                  )

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Insights","Predict Weekly Sales"], 
                           icons=["house","graph-up-arrow","gear"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font": "sans serif","font-size": "20px", "text-align": "centre"},
                                   "nav-link-selected": {"font": "sans serif", "background-color": "#A020F0"},
                                   "icon": {"font-size": "20px"}
                                   }
                          )
# READING THE CLEANED DATAFRAME
df = pd.read_csv('Cleaned_Store_data2.csv')


# HOME PAGE
if selected == "Home":
    
    st.markdown("# :red[Retail Sales Forecasting]")
    st.markdown("## :blue[Overview] : This project aims to leverage machine learning techniques to predict department-wide sales for each store in the upcoming year. It will model the effects of markdowns during holiday weeks to understand their influence on sales. Insights will be visualized using Streamlit, providing an interactive platform for exploring sales patterns and predictions. The project integrates predictive modeling, causal analysis, and data-driven decision-making for strategic retail optimization. ")
    st.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, EDA, Model Building, Model Deployment, Streamlit")
    

# OVERVIEW PAGE
if selected == "Insights":
    st.markdown("## Insights of Retail Store")
    
    # DATAFRAME FORMAT
    if st.button("Click to view Dataframe"):
        st.write(df)
    
    # GETTING USER INPUTS
    month = st.sidebar.multiselect('Select a Month', sorted(df.Month.unique()), sorted(df.Month.unique()))
    year = st.sidebar.multiselect('Select Year', sorted(df.Year.unique()), sorted(df.Year.unique()))
    store = st.sidebar.multiselect('Select Store', sorted(df.Store.unique()), sorted(df.Store.unique()))
    dept = st.sidebar.multiselect('Select Dept', sorted(df.Dept.unique()), sorted(df.Dept.unique()))
    
    # SELECT OPTION TO EXPLORE
    choice = st.selectbox("**Select an option to Explore their data**", 
                           ['Explore of Weekly Sales', 'Explore of Markdown'])
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f"Month in {month} & Year in {year} & Store in {store} & Dept in {dept}"
    
    if choice == 'Explore of Weekly Sales':
        
# Filter the data based on the query
            filtered_df = df.query(query)
            st.markdown("## :rainbow[Stores and their Sum of Weekly Sales]")
# Group by Store and calculate the sum of Weekly Sales and Markdown
            sales = filtered_df.groupby(['Store'])[['Weekly_Sales', 'Markdown']].sum().reset_index()
            
# Create a horizontal bar chart using Plotly
            fig = px.bar(
                sales,
                x='Weekly_Sales',
                y='Store',
#title="Stores and their Sum of Weekly Sales",
                orientation='h',
                color='Markdown', 
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={"Weekly_Sales": "Weekly Sales", "Store": "Store"},
            )
            
# Display the chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)



# Top 10 Stores with the Highest Sales
            st.markdown("## :rainbow[Top 10 Stores with the Highest Sales]")
            highest_sale = filtered_df.groupby(['Store'])['Weekly_Sales'].sum().reset_index().sort_values('Weekly_Sales', ascending=False).head(10)
            fig_highest_store = px.bar(
                highest_sale,
                x='Weekly_Sales',
                y='Store',
#title="Top 10 Stores with the Highest Sales",
                orientation='h',
                color='Weekly_Sales',
                color_continuous_scale=px.colors.sequential.Aggrnyl,
                labels={"Weekly_Sales": "Weekly Sales", "Store": "Store"}
            )
            st.plotly_chart(fig_highest_store, use_container_width=True)

# Top 10 Stores with the Lowest Sales
            st.markdown("## :rainbow[Top 10 Stores with the Lowest Sales]")
            lowest_sale = filtered_df.groupby(['Store'])['Weekly_Sales'].sum().reset_index().sort_values('Weekly_Sales', ascending=True).head(10)
            fig_lowest_store = px.bar(
                lowest_sale,
                x='Weekly_Sales',
                y='Store',
#title="Top 10 Stores with the Lowest Sales",
                orientation='h',
                color='Weekly_Sales',
                color_continuous_scale=px.colors.sequential.Purp,
                labels={"Weekly_Sales": "Weekly Sales", "Store": "Store"}
            )
            st.plotly_chart(fig_lowest_store, use_container_width=True)

# Department and their Sum of Weekly Sales
            st.markdown("## :rainbow[Department and their Sum of Weekly Sales]")
            dept_sales = filtered_df.groupby(['Dept'])['Weekly_Sales'].sum().reset_index()
            fig_dept_sales = px.bar(
                dept_sales,
                x='Weekly_Sales',
                y='Dept',
#title="Departments and their Total Weekly Sales",
                orientation='h',
                color='Weekly_Sales',
                color_continuous_scale=px.colors.sequential.Sunset,
                labels={"Weekly_Sales": "Weekly Sales", "Dept": "Department"}
            )
            st.plotly_chart(fig_dept_sales, use_container_width=True)

# Top 10 Departments with the Highest Sales
            st.markdown("## :rainbow[Top 10 Departments with the Highest Sales]")
            highest_dept_sale = filtered_df.groupby(['Dept'])['Weekly_Sales'].sum().reset_index().sort_values('Weekly_Sales', ascending=False).head(10)
            fig_highest_dept = px.bar(
                highest_dept_sale,
                x='Weekly_Sales',
                y='Dept',
#title="Top 10 Departments with the Highest Sales",
                orientation='h',
                color='Weekly_Sales',
                color_continuous_scale=px.colors.sequential.Agsunset,
                labels={"Weekly_Sales": "Weekly Sales", "Dept": "Department"}
            )
            st.plotly_chart(fig_highest_dept, use_container_width=True)

# Top 10 Departments with the Lowest Sales
            st.markdown("## :rainbow[Top 10 Departments with the Lowest Sales]")
            lowest_dept_sale = filtered_df.groupby(['Dept'])['Weekly_Sales'].sum().reset_index().sort_values('Weekly_Sales', ascending=True).head(10)
            fig_lowest_dept = px.bar(
                lowest_dept_sale,
                x='Weekly_Sales',
                y='Dept',
#title="Top 10 Departments with the Lowest Sales",
                orientation='h',
                color='Weekly_Sales',
                color_continuous_scale=px.colors.sequential.Blues,
                labels={"Weekly_Sales": "Weekly Sales", "Dept": "Department"}
            )
            st.plotly_chart(fig_lowest_dept, use_container_width=True)

    elif choice == 'Explore of Markdown':
            
# Filter the data based on the query
            filtered_df = df.query(query)
# Markdown by Store
            st.markdown("## :rainbow[Stores and their Sum of Markdown]")
            store_markdown_sales = filtered_df.groupby(['Store'])[['Markdown', 'Weekly_Sales']].sum().reset_index()
            fig_store_markdown = px.bar(
                store_markdown_sales,
                x='Markdown',
                y='Store',
#title="Stores and their Sum of Markdown",
                orientation='h',
                color='Weekly_Sales',
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={"Markdown": "Markdown", "Store": "Store"}
            )
            st.plotly_chart(fig_store_markdown, use_container_width=True)

# Top 10 Stores with Highest Markdown
            st.markdown("## :rainbow[Top 10 Stores with the Highest Markdown]")
            highest_markdown = filtered_df.groupby(['Store'])['Markdown'].sum().reset_index().sort_values('Markdown', ascending=False).head(10)

            fig_top_high_markdown = px.bar(
#top_10_high_markdown_stores,
                highest_markdown,
                x='Markdown',
                y='Store',
#title="Top 10 Stores with the Highest Markdown",
                orientation='h',
                color='Markdown',
                color_continuous_scale=px.colors.sequential.Plasma,
                labels={"Markdown": "Markdown", "Store": "Store"}
            )
            st.plotly_chart(fig_top_high_markdown, use_container_width=True)
    
# Top 10 Stores with Lowest Markdown
            st.markdown("## :rainbow[Top 10 Stores with the Lowest Markdown]")
            lowest_markdown = filtered_df.groupby(['Store'])['Markdown'].sum().reset_index().sort_values('Markdown', ascending=False).head(10)

            fig_top_low_markdown = px.bar(
#top_10_low_markdown_stores,
                lowest_markdown,
                x='Markdown',
                y='Store',
#title="Top 10 Stores with the Lowest Markdown",
                orientation='h',
                color='Markdown',
                color_continuous_scale=px.colors.sequential.Blues,
                labels={"Markdown": "Markdown", "Store": "Store"}
            )
            st.plotly_chart(fig_top_low_markdown, use_container_width=True)

# Markdown by Department
            st.markdown("## :rainbow[Departments and their Sum of Markdown]")
            
            dept_markdown_sales = filtered_df.groupby(['Dept'])['Markdown'].sum().reset_index()

            fig_dept_markdown = px.bar(
                dept_markdown_sales,
                x='Markdown',
                y='Dept',
#title="Departments and their Sum of Markdown",
                orientation='h',
                color='Markdown',
                color_continuous_scale=px.colors.sequential.Sunset,
                labels={"Markdown": "Markdown", "Dept": "Department"}
            )
            st.plotly_chart(fig_dept_markdown, use_container_width=True)

# Top 10 Departments with Highest Markdown
            st.markdown("## :rainbow[Top 10 Departments with the Highest Markdown]")
            top_10_high_markdown_dept = filtered_df.groupby(['Dept'])['Markdown'].sum().reset_index().sort_values('Markdown', ascending=False).head(10)
            
            
            fig_top_high_markdown_dept = px.bar(
                top_10_high_markdown_dept,
                x='Markdown',
                y='Dept',
#title="Top 10 Departments with the Highest Markdown",
                orientation='h',
                color='Markdown',
                color_continuous_scale=px.colors.sequential.Agsunset,
                labels={"Markdown": "Markdown", "Dept": "Department"}
            )
            st.plotly_chart(fig_top_high_markdown_dept, use_container_width=True)

# Top 10 Departments with Lowest Markdown
            st.markdown("## :rainbow[Top 10 Departments with the Lowest Markdown]")
            top_10_low_markdown_dept = filtered_df.groupby(['Dept'])['Markdown'].sum().reset_index().sort_values('Markdown', ascending=False).head(10)
            
            fig_top_low_markdown_dept = px.bar(
                top_10_low_markdown_dept,
                x='Markdown',
                y='Dept',
#title="Top 10 Departments with the Lowest Markdown",
                orientation='h',
                color='Markdown',
                color_continuous_scale=px.colors.sequential.Teal,
                labels={"Markdown": "Markdown", "Dept": "Department"}
            )
            st.plotly_chart(fig_top_low_markdown_dept, use_container_width=True)

if selected == "Predict Weekly Sales":
    def load_data():
        df = pd.read_csv('Cleaned_Store_data2.csv')
        return df

    # Load data
    df = load_data()
    x = df.drop(['Size', 'Type', 'weekly_sales'], axis=1)

    # Form for user input
    with st.form(key='form', clear_on_submit=False):
        store = st.selectbox("**Select a Store**", options=df['Store'].unique())
        dept = st.selectbox("**Select a Department**", options=df['Dept'].unique())
        holiday = st.radio("**Click Holiday is True or False**", options=[True, False], horizontal=True)

        temperature = st.number_input(
            f"**Enter a Temperature in range of (Minimum: {df['Temperature'].min()} & Maximum: {df['Temperature'].max()})**",
        )

        fuel = st.number_input(
            f"**Enter a Fuel Price in range of (Minimum: {df['Fuel_Price'].min()} & Maximum: {df['Fuel_Price'].max()})**",
        )

        cpi = st.number_input(
            f"**Enter a Customer Price Index in range of (Minimum: {df['CPI'].min()} & Maximum: {df['CPI'].max()})**",
        )

        unemployment = st.number_input(
            f"**Enter an Unemployment in range of (Minimum: {df['Unemployment'].min()} & Maximum: {df['Unemployment'].max()})**",
        )

        year = st.selectbox("**Select a Year**", options=[2010, 2011, 2012, 2013, 2014])
        month = st.selectbox("**Select a Month**", options=df['Month'].unique())

        markdown = st.number_input(
            f"**Enter a Markdown value in range of (Minimum: {df['Markdown'].min()} & Maximum: {df['Markdown'].max()})**",
        )

# Helper functions
        def inv_trans(x):
            return 1 / x if x != 0 else x

        def is_holiday(x):
            return 1 if x else 0

# Form submit button
        button = st.form_submit_button("**Predict**", use_container_width=True)

    if button:
# Preprocess inputs
        processed_input = {
            'Month': month,
            'Year': year,
            'Store': store,
            'Dept': dept,
            'IsHoliday': is_holiday(holiday),
            'Temperature': temperature,
            'Fuel_Price': fuel,
            'CPI': cpi,
            'Unemployment': unemployment,
            'Markdown': inv_trans(markdown),
        }

# Convert input to DataFrame
        input_df = pd.DataFrame([processed_input])

# Load model and predict
        try:
            with open('RandomForestRegressorr.pkl', 'rb') as file:
                model = pickle.load(file)
                result = model.predict(input_df)[0]
                st.markdown(f"## :green[*Predicted Weekly Sales is {result:.2f}*]")
        except Exception as e:
            st.error(f"Error: {e}")


        
    
    