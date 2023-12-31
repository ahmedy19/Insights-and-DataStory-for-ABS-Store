# Insights_for_ABS_Store

# Import required packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from google.colab import drive
drive.mount('/content/drive')

## Load datasets

path = r'/content/drive/MyDrive/datasets/ABS_Store_Inventory_and_alcohol_liquor_Sales.csv'
df = pd.read_csv(path, low_memory=False)

df.shape

df.sample(10)

df.dtypes

df.isnull().sum()

# Since there are 12447 null value in `Sale Price` and `Sale End Date` columns, so it's better to remove them

df.drop(['Sale Price', 'Sale End Date'], inplace=True, axis=1)

df['Category'].value_counts()

df['Category'].unique()

# Fill the missing values in the `Category` column

most_frequent_category = df['Category'].mode()[0]
df['Category'].fillna(most_frequent_category, inplace=True)

# Change the object data type columns to category data type

df = df.astype({'Category':'category', 'Description':'category', 'Size':'category'})

df.dtypes

df.info()

df.describe().T

# Check the duplicated rows

df.duplicated().sum()

# Check if there are outliers in the dataset and remove them

fig1 = px.box(df, y='Total Inventory', title='<b>Box Plot: Total Inventory</b>')
fig2 = px.box(df, y='Price', title='<b>Box Plot: Prices</b>')

fig1.show()
fig2.show()

# Check if there are outliers in the dataset and remove them

# Seaborn Package

plt.figure(figsize=(20, 10))

sns.boxplot(data=df, y='Total Inventory', color='skyblue', showmeans=True, meanline=True)
plt.title('Box Plot: Total Inventory')
plt.xlabel('')
plt.ylabel('Total Inventory')
plt.show()

plt.figure(figsize=(20, 10))
sns.boxplot(data=df, y='Price', color='lightgreen', showmeans=True, meanline=True)
plt.title('Box Plot: Prices')
plt.xlabel('')
plt.ylabel('Price')
plt.show()

# Define the columns for outlier removal

columns_to_remove_outliers = ['Total Inventory', 'Price']

cleaned_df = df.copy()

for column in columns_to_remove_outliers:
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    cleaned_df = cleaned_df[(cleaned_df[column] >= lower_bound) & (cleaned_df[column] <= upper_bound)]

cleaned_df.shape

cleaned_df.dtypes

cleaned_df.info()

cleaned_df.describe().T

# Export Cleaned Dataset
cleaned_df.to_csv('Cleaned_ABS_Store_Inventory_and_alcohol_liquor_Sales.csv', index=False)

# Insight-1: Which category of alcohol has the highest total inventory?

# This plot using Plotly package

inventory_by_category = cleaned_df.groupby('Category')['Total Inventory'].sum().sort_values(ascending=False).reset_index()

highest_inventory_category = inventory_by_category.loc[inventory_by_category['Total Inventory'].idxmax(), 'Category']

print("Category with the highest total inventory:", highest_inventory_category)

fig = px.bar(inventory_by_category, x='Category', y='Total Inventory',
             title='<b>Which category of alcohol has the highest total inventory?<br>(Total Inventory by Category)</b>',
             labels={'Total Inventory': '<b>Inventory</b>'})

fig.update_layout(xaxis_title='<b>Category</b>', yaxis_title='<b>Total Inventory</b>')

fig.show()

# Insight-1: Which category of alcohol has the highest total inventory?

# This plot using Seaborn package

inventory_by_category = cleaned_df.groupby('Category')['Total Inventory'].sum().sort_values(ascending=False).reset_index()

highest_inventory_category = inventory_by_category.loc[inventory_by_category['Total Inventory'].idxmax(), 'Category']

print("Category with the highest total inventory:", highest_inventory_category)

plt.figure(figsize=(20, 10))

sns.barplot(data=inventory_by_category, x='Category', y='Total Inventory', order=inventory_by_category.sort_values('Total Inventory', ascending=False)['Category'])
plt.title('Which category of alcohol has the highest total inventory?\n(Total Inventory by Category)')
plt.xlabel('Category')
plt.ylabel('Total Inventory')
plt.xticks(rotation=90)

plt.show()

# Insight-2: What is the average price of alcohol products in each category?

# This plot using Plotly package

average_price_by_category = cleaned_df.groupby('Category')['Price'].mean().sort_values(ascending=False).reset_index()

colors = px.colors.qualitative.Plotly

fig = px.bar(average_price_by_category, x='Category', y='Price', title='<b>What is the average price of alcohol products in each category?<br>(Average Price by Category)</b>',
             labels={'Price': 'Average Price'}, color='Category',
             color_discrete_sequence=colors)

fig.update_layout(xaxis_title='<b>Category</b>', yaxis_title='<b>Average Price</b>')

fig.show()

# Insight-2: What is the average price of alcohol products in each category?

# This plot using Seaborn package

average_price_by_category = cleaned_df.groupby('Category')['Price'].mean().reset_index()

plt.figure(figsize=(20, 10))

sns.barplot(data=average_price_by_category, x='Category', y='Price', palette='viridis', order=average_price_by_category.sort_values('Price', ascending=False)['Category'])
plt.title('What is the average price of alcohol products in each category?\n(Average Price by Category)')
plt.xlabel('Category')
plt.ylabel('Average Price')
plt.xticks(rotation=90)

plt.show()

average_price_by_category.sort_values(by='Price', ascending=False)

# Insight-3: How does the inventory distribution vary across different sizes of alcohol products?

# This plot using Plotly package

inventory_distribution = cleaned_df.groupby('Size')['Total Inventory'].describe().reset_index()
colors = px.colors.qualitative.Plotly

fig = px.bar(inventory_distribution, x='Size', y='count', title='<b>Inventory Distribution by Size</b>',
             labels={'Size': '<b>Alcohol Size</b>', 'count': '<b>Inventory Count</b>'}, color='Size',
             color_discrete_sequence=colors)

fig.update_layout(xaxis_title='<b>Size</b>', yaxis_title='<b>Inventory Count</b>')

fig.show()

# Insight-3: How does the inventory distribution vary across different sizes of alcohol products?

# This plot using Seaborn package

inventory_distribution = cleaned_df.groupby('Size')['Total Inventory'].count().reset_index()

plt.figure(figsize=(20, 10))

sns.barplot(data=inventory_distribution, x='Size', y='Total Inventory', palette='viridis', order=inventory_distribution.sort_values('Total Inventory', ascending=False)['Size'])
plt.title('Inventory Distribution by Size')
plt.xlabel('Alcohol Size')
plt.ylabel('Inventory Count')
plt.xticks(rotation=90)

plt.show()

inventory_distribution.sort_values(by='Total Inventory', ascending=False)

# Insight-4: Are there any correlations between the price and total inventory of alcohol products?

# This plot using Plotly package


fig = px.scatter(cleaned_df, x='Price', y='Total Inventory', title='<b>Are there any correlations between the price and total inventory of alcohol products?<br>(Correlation: Price vs Total Inventory)</b>',
                 labels={'Price': '<b>Price</b>', 'Total Inventory': '<b>Total Inventory</b>'},
                 color='Total Inventory')

fig.show()

# Insight-4: Are there any correlations between the price and total inventory of alcohol products?

# This plot using Seaborn package

plt.figure(figsize=(20, 10))

sns.scatterplot(data=cleaned_df, x='Price', y='Total Inventory', hue='Total Inventory', palette='viridis')
plt.title('Correlation: Price vs Total Inventory')
plt.xlabel('Price')
plt.ylabel('Total Inventory')
plt.xticks(rotation=90)

plt.show()

# Insight-5: Which specific alcohol product has the highest price?

# This plot using Plotly package

highest_price_product = cleaned_df.loc[cleaned_df['Price'].idxmax()]
highest_price = highest_price_product['Price']
product_name = highest_price_product['Description']

highest_price_df = pd.DataFrame({'Description': [product_name], 'Price': [highest_price]})

colors = px.colors.qualitative.Plotly

fig = px.bar(highest_price_df, x='Description', y='Price', title='<b>Which specific alcohol product has the highest price?<br>(Alcohol Product with Highest Price)</b>',
             labels={'Description': '<b>Product</b>', 'Price': '<b>Price</b>'}, color='Description',
             color_discrete_sequence=colors)

fig.update_layout(xaxis_title='<b>Product</b>', yaxis_title='<b>Price</b>')

fig.show()

# Insight-5: Which specific alcohol product has the highest price?

# This plot using Seaborn package

plt.figure(figsize=(20, 10))

highest_price_product = cleaned_df.loc[cleaned_df['Price'].idxmax()]
highest_price = highest_price_product['Price']
product_name = highest_price_product['Description']

sns.barplot(x=[product_name], y=[highest_price], color='blue')

plt.title('Alcohol Product with Highest Price')
plt.xlabel('Product')
plt.ylabel('Price')
plt.xticks(rotation=90)

plt.show()

highest_price_product

# Insight-6: How does the average price differ between different sizes of alcohol products?

# This plot using Plotly package

average_price_by_size = cleaned_df.groupby('Size')['Price'].mean().sort_values(ascending=False).reset_index()

colors = px.colors.qualitative.Plotly

fig = px.bar(average_price_by_size, x='Size', y='Price', title='<b>How does the average price differ between different sizes of alcohol products?<br>(Average Price by Size)</b>',
             labels={'Size': '<b>Alcohol Size</b>', 'Price': '<b>Average Price</b>'}, color='Size',
             color_discrete_sequence=colors)

fig.update_layout(xaxis_title='<b>Size</b>', yaxis_title='<b>Average Price</b>')

fig.show()

# Insight-6: How does the average price differ between different sizes of alcohol products?

# This plot using Seborn package

average_price_by_size = cleaned_df.groupby('Size')['Price'].mean().sort_values(ascending=False).reset_index()

plt.figure(figsize=(20, 10))
sns.barplot(data=average_price_by_size, x='Size', y='Price', order=average_price_by_size['Size'], palette='Set3')

plt.title('Average Price by Size')
plt.xlabel('Alcohol Size')
plt.ylabel('Average Price')
plt.xticks(rotation=90)

plt.show()

average_price_by_size.sort_values(by='Price', ascending=False)

# Insight-7: Which category of alcohol has the highest average price?

# This plot using Plotly package


average_price_by_category = cleaned_df.groupby('Category')['Price'].mean().reset_index()

highest_average_price_category = average_price_by_category.loc[average_price_by_category['Price'].idxmax(), 'Category']

highest_average_price_category_df = average_price_by_category[average_price_by_category['Category'] == highest_average_price_category]

colors = px.colors.qualitative.Plotly

fig = px.bar(highest_average_price_category_df, x='Category', y='Price', title='<b>Which category of alcohol has the highest average price?<br>(Category with Highest Average Price)</b>',
             labels={'Category': '<b>Alcohol Category</b>', 'Price': '<b>Average Price</b>'}, color='Category',
             color_discrete_sequence=colors)

fig.update_layout(xaxis_title='<b>Category</b>', yaxis_title='<b>Average Price</b>')

fig.show()

# Insight-7: Which category of alcohol has the highest average price?

# This plot using Seaborn package

average_price_by_category = cleaned_df.groupby('Category')['Price'].mean().reset_index()
highest_average_price_category = average_price_by_category.loc[average_price_by_category['Price'].idxmax(), 'Category']
highest_average_price_category_df = average_price_by_category[average_price_by_category['Category'] == highest_average_price_category]

plt.figure(figsize=(20, 10))

sns.barplot(data=highest_average_price_category_df, x='Category', y='Price', palette='Set3')

plt.title('Category with Highest Average Price')
plt.xlabel('Alcohol Category')
plt.ylabel('Average Price')
plt.xticks(rotation=90)

plt.show()

highest_average_price_category_df

# Insight-8: Which category of alcohol has the highest demand based on the total inventory and price?

# This plot using Plotly package

cleaned_df['Demand'] = cleaned_df['Total Inventory'] * cleaned_df['Price']

highest_demand_category = cleaned_df.groupby('Category')['Demand'].sum().idxmax()

highest_demand_category_df = cleaned_df[cleaned_df['Category'] == highest_demand_category]

fig = px.scatter(highest_demand_category_df, x='Total Inventory', y='Price', title='<b>Which category of alcohol has the highest demand based on the total inventory and price?<br>(Category with Highest Demand)</b>',
                 labels={'Total Inventory': '<b>Total Inventory</b>', 'Price': '<b>Price</b>'},
                  color='Category')

fig.update_layout(xaxis_title='<b>Total Inventory</b>', yaxis_title='<b>Price</b>')

fig.show()

# Insight-8: Which category of alcohol has the highest demand based on the total inventory and price?

# This plot using Seaborn package

cleaned_df['Demand'] = cleaned_df['Total Inventory'] * cleaned_df['Price']

highest_demand_category = cleaned_df.groupby('Category')['Demand'].sum().idxmax()

highest_demand_category_df = cleaned_df[cleaned_df['Category'] == highest_demand_category]

plt.figure(figsize=(20, 10))

sns.scatterplot(data=highest_demand_category_df, x='Total Inventory', y='Price', hue='Category')
plt.title('Which category of alcohol has the highest demand based on the total inventory and price?\n(Category with Highest Demand)')
plt.xlabel('Total Inventory')
plt.ylabel('Price')
plt.xticks(rotation=90)

plt.show()

highest_demand_category

# Insight-9: How does the price and inventory vary for different descriptions within each category?

# This plot using Plotly package

category_description_stats = cleaned_df.groupby(['Category', 'Description']).agg({'Price': 'mean', 'Total Inventory': 'sum'}).reset_index()

colors = px.colors.qualitative.Plotly

fig = px.scatter(category_description_stats, x='Price', y='Total Inventory', color='Category', hover_data=['Description'],
                 title='<b>How does the price and inventory vary for different descriptions within each category?<br>(Price and Inventory Variation by Description)</b>', labels={'Price': '<b>Average Price</b>', 'Total Inventory': '<b>Total Inventory</b>'},
                 color_discrete_sequence=colors)

fig.update_layout(xaxis_title='<b>Average Price</b>', yaxis_title='<b>Total Inventory</b>')

fig.show()

# Insight-9: How does the price and inventory vary for different descriptions within each category?

# This plot using Seaborn package

category_description_stats = cleaned_df.groupby(['Category', 'Description']).agg({'Price': 'mean', 'Total Inventory': 'sum'}).reset_index()

plt.figure(figsize=(20, 10))

sns.scatterplot(data=category_description_stats, x='Price', y='Total Inventory', hue='Category')
plt.title('How does the price and inventory vary for different descriptions within each category?\n(Price and Inventory Variation by Description)')
plt.xlabel('Average Price')
plt.ylabel('Total Inventory')
plt.xticks(rotation=90)

plt.show()

# Calculate the total price for each category and sort them in descending order
category_prices = cleaned_df.groupby('Category')['Price'].sum().sort_values(ascending=False)
category_prices

# Calculate the average price for each category sort them in descending order
category_prices = cleaned_df.groupby('Category')['Price'].mean().sort_values(ascending=False)
category_prices

# Calculate the average price for each category

# This plot using Plotly package

category_prices = cleaned_df.groupby('Category')['Price'].mean().reset_index()
sorted_categories = category_prices.sort_values('Price', ascending=False)
top_five_categories = sorted_categories.head(5)

fig = px.pie(top_five_categories, values='Price', names='Category', title='Top Five Categories by Average Price')

fig.show()

# Calculate the average price for each category

# This plot using Seaborn package

category_prices = cleaned_df.groupby('Category')['Price'].mean().reset_index()
sorted_categories = category_prices.sort_values('Price', ascending=False)
top_five_categories = sorted_categories.head(5)

plt.figure(figsize=(20, 10))
plt.pie(top_five_categories['Price'], labels=top_five_categories['Category'], autopct='%1.1f%%')
plt.title('Top Five Categories by Average Price')

plt.show()

# Find the product with the highest price

highest_price_row = cleaned_df[cleaned_df['Price'] == cleaned_df['Price'].max()]

highest_price_description = highest_price_row['Description'].values[0]

print("Description of the highest-priced item:", highest_price_description)
print("Price of the highest-priced item:", highest_price)

# List Categories and its products

category_description_df = cleaned_df.groupby('Category').agg({'Description': lambda x: list(x)})

category_description_df = category_description_df.reset_index()

category_description_df

# Count how many product in each category and list them in descending order

category_description_df = cleaned_df.groupby('Category').agg({'Description': lambda x: list(x)})
category_description_df = category_description_df.reset_index()

category_description_df['Description Count'] = category_description_df['Description'].apply(len)
sorted_category_description_df = category_description_df.sort_values('Description Count', ascending=False)

sorted_category_description_df

# Highest priced products in categories

highest_price_rows = cleaned_df.groupby('Category').apply(lambda x: x[x['Price'] == x['Price'].max()])

highest_price_rows = highest_price_rows.reset_index(drop=True)

highest_price_product_info = highest_price_rows.sort_values('Price', ascending=False)

highest_price_product_info

highest_price_row = cleaned_df.loc[cleaned_df['Price'].idxmax()]

highest_inventory_row = cleaned_df.loc[cleaned_df['Total Inventory'].idxmax()]

highest_rows_df = pd.concat([highest_price_row, highest_inventory_row], axis=1).T

sorted_highest_rows_df = highest_rows_df.sort_values(['Price', 'Total Inventory'], ascending=False)

result = sorted_highest_rows_df[['Description', 'Category', 'Price', 'Total Inventory']]

result

highest_inventory_row = cleaned_df.loc[cleaned_df['Total Inventory'].idxmax()]

product_name = highest_inventory_row['Description']
category = highest_inventory_row['Category']
highest_total_amount = highest_inventory_row['Total Inventory']

print("Product Name:", product_name)
print("Category:", category)
print("Highest Total Amount in an Inventory:", highest_total_amount)

highest_price_row = cleaned_df.loc[cleaned_df['Price'].idxmax()]

highest_price = highest_price_row['Price']
total_inventory = highest_price_row['Total Inventory']

total_amount = highest_price * total_inventory

print("Total Amount in Inventory of Highest-Priced Product:", total_amount)

highest_price_row

# Highest demand Product size

highest_demand = cleaned_df['Demand'].max()

highest_demand_sizes = cleaned_df.loc[cleaned_df['Demand'] == highest_demand, 'Size'].unique()

print("Highest Demand Size:", highest_demand_sizes[0])

