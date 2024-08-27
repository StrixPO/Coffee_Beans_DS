import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = './dataset/Raw Data.xlsx'
xls = pd.ExcelFile(file_path)
df_orders = pd.read_excel(xls, 'orders')
df_customers = pd.read_excel(xls, 'customers')
df_products = pd.read_excel(xls, 'products')

# CLean null values
df_customers_cleaned = df_customers.dropna(subset=['Email', 'Phone Number'])

# clean redundant null columns in orders sheet
df_orders_cleaned = df_orders.drop(columns=['Customer Name', 'Email', 'Country', 'Coffee Type', 'Roast Type', 'Size', 'Unit Price', 'Sales'])

# Change 'Order Date' to datetime datatype
df_orders_cleaned['Order Date'] = pd.to_datetime(df_orders_cleaned['Order Date'], format= '%d/%m/%Y')
#merge the three sheets to create a complete dataframe
df_orders_customers = pd.merge(df_orders_cleaned, df_customers_cleaned, on='Customer ID', how='left')
df_complete = pd.merge(df_orders_customers, df_products, on='Product ID', how='left')


# Calculate Sales column 
df_complete['Sales'] = df_complete['Quantity'] * df_complete['Unit Price']

# Set the title of the web app
st.title("Coffee Bean Sales Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose a page", ["Home", "Sales Over Time", "Top Products", "Customer Segmentation"])

# Define pages
if option == "Home":
    st.write("Welcome to the Coffee Bean Sales Analysis App!")
    st.write("Use the sidebar to navigate through different analyses.")

# plot with streamlit
elif option == "Sales Over Time":
    st.header("Sales Over Time")
    sales_over_time = df_complete.groupby('Order Date')['Sales'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.plot(sales_over_time['Order Date'], sales_over_time['Sales'], marker='o')
    ax.set_title('Sales Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    st.pyplot(fig)

# plot with streamlit
elif option == "Top Products":
    st.header("Top Products by Sales")
    top_products = df_complete.groupby('Product ID')['Sales'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    top_products.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Top 10 Products by Sales')
    ax.set_xlabel('Product ID')
    ax.set_ylabel('Total Sales')
    st.pyplot(fig)

# plot with streamlit
elif option == "Customer Segmentation":
    st.header("Customer Segmentation")
    customer_spending = df_complete.groupby('Customer ID')['Sales'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.hist(customer_spending['Sales'], bins=30, color='orange', edgecolor='k')
    ax.set_title('Distribution of Customer Spending')
    ax.set_xlabel('Total Spending')
    ax.set_ylabel('Number of Customers')
    st.pyplot(fig)
