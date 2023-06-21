# Import required packages 
import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff


# Load dataset
path = r'datasets/Cleaned_ABS_Store_Inventory_and_alcohol_liquor_Sales.csv'
df = pd.read_csv(path, low_memory=False)

st.set_page_config(
    page_title="Insights and Storytelling Dashboard for ABS Store",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# dashboard title
st.title("Insights and Storytelling Dashboard for ABS Store")


# dashboard title
st.subheader('Prepared by: Ahmed Yaseen')

st.markdown("---")


# top-level filters 
category_filter = st.selectbox("Category", pd.unique(df['Category']))


# creating a single-element container.
placeholder = st.empty()

# dataframe filter 
df = df[df['Category']==category_filter]


for seconds in range(200):

    inventory_distribution = df.groupby('Size')['Total Inventory'].describe().reset_index()
    
    highest_price_product = df.loc[df['Price'].idxmax()]
    highest_price = highest_price_product['Price']
    product_name = highest_price_product['Description']
    highest_price_df = pd.DataFrame({'Description': [product_name], 'Price': [highest_price]})
    
    average_price_by_size = df.groupby('Size')['Price'].mean().sort_values(ascending=False).reset_index()
    
    category_description_stats = df.groupby(['Category', 'Description']).agg({'Price': 'mean', 'Total Inventory': 'sum'}).reset_index()
    
    common_sizes_by_category = df.groupby('Size')['Price'].mean().sort_values(ascending=False).reset_index()
        

    with placeholder.container():
        
        # create 1 column for charts 
        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            
            st.markdown("### Insight 1")
            
            fig = px.bar(inventory_distribution, x='Size', y='count', title='<b>Inventory Distribution by Size</b>',
             labels={'Size': '<b>Alcohol Size</b>', 'count': '<b>Inventory Count</b>'}, color='Size',
             color_discrete_sequence=px.colors.qualitative.Plotly)

            fig.update_layout(xaxis_title='<b>Size</b>', yaxis_title='<b>Inventory Count</b>', xaxis_tickangle=-45)
            
            st.write(fig)
            
        
        with fig_col2:
            st.markdown("### Insight 2")
                     
            fig = px.scatter(df, x='Price', y='Total Inventory', title='<b>Are there any correlations between the price and total inventory of alcohol products?<br>(Correlation: Price vs Total Inventory)</b>',
                 labels={'Price': '<b>Price</b>', 'Total Inventory': '<b>Total Inventory</b>'},
                 color='Total Inventory')

            fig.update_layout(xaxis_tickangle=-45)
            
            st.write(fig)
            
        
        with fig_col1:
            
            st.markdown("### Insight 3")
            
            fig = px.bar(highest_price_df, x='Description', y='Price', title='<b>Which specific alcohol product has the highest price?<br>(Alcohol Product with Highest Price)</b>',
             labels={'Description': '<b>Product</b>', 'Price': '<b>Price</b>'}, color='Description',
             color_discrete_sequence=px.colors.qualitative.Plotly)

            fig.update_layout(xaxis_title='<b>Product</b>', yaxis_title='<b>Price</b>', xaxis_tickangle=-45)
            
            st.write(fig)
            
        
        with fig_col2:
            st.markdown("### Insight 4")
                     
            fig = px.bar(average_price_by_size, x='Size', y='Price', title='<b>How does the average price differ between different sizes of alcohol products?<br>(Average Price by Size)</b>',
             labels={'Size': '<b>Alcohol Size</b>', 'Price': '<b>Average Price</b>'}, color='Size',
             color_discrete_sequence=px.colors.qualitative.Plotly)

            fig.update_layout(xaxis_title='<b>Size</b>', yaxis_title='<b>Average Price</b>')
            
            st.write(fig)
            
        
        with fig_col1:
            
            st.markdown("### Insight 5")
            
            fig = px.scatter(category_description_stats, x='Price', y='Total Inventory', color='Category', hover_data=['Description'],
                            title='<b>How does the price and inventory vary for different descriptions within each category?<br>(Price and Inventory Variation by Description)</b>', labels={'Price': '<b>Average Price</b>', 'Total Inventory': '<b>Total Inventory</b>'},
                            color_discrete_sequence=px.colors.qualitative.Plotly)

            fig.update_layout(xaxis_title='<b>Average Price</b>', yaxis_title='<b>Total Inventory</b>', xaxis_tickangle=-45)
            
            st.write(fig)
            
        
        with fig_col2:
            st.markdown("### Insight 6")

            fig = px.bar(common_sizes_by_category, x='Size', y='Price', color='Price',
                        title='<b>Common Sizes by Category with their Prices</b>',
                        labels={'Size': '<b>Size</b>', 'Price': '<b>Price</b>'},
                        color_discrete_sequence=px.colors.qualitative.Plotly)

            fig.update_layout(xaxis_title='<b>Size</b>', yaxis_title='<b>Price</b>', xaxis_tickangle=-45)

            st.write(fig)
            
        
        
        
        
        st.markdown("---")
            
               
        st.markdown("### Data")
        num_rows = len(df) - 1
        st.dataframe(df.head(num_rows))
        time.sleep(1)
        

