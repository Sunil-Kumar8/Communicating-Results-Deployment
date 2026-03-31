import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analytics Dashboard", page_icon="📈", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('ecommerce_sales_data.csv')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run PROJECT.py first to generate 'ecommerce_sales_data.csv'.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.title("📈 Business Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar Filters
    st.sidebar.header("Dashboard Filters")
    selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
    selected_category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())
    
    # Filter Data
    filtered_df = df[(df['Region'].isin(selected_region)) & (df['Category'].isin(selected_category))]
    
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Calculate KPIs
        total_sales = filtered_df['Sales'].sum()
        total_profit = filtered_df['Profit'].sum()
        num_orders = len(filtered_df)
        
        filtered_df['Month'] = filtered_df['Order Date'].dt.to_period('M')
        monthly_sales = filtered_df.groupby('Month')['Sales'].sum()
        growth_rate = 0
        if len(monthly_sales) > 1:
            growth_rate = ((monthly_sales.iloc[-1] - monthly_sales.iloc[-2]) / monthly_sales.iloc[-2]) * 100
            
        top_region = filtered_df.groupby('Region')['Sales'].sum().idxmax() if not filtered_df.empty else "N/A"
        best_category = filtered_df.groupby('Category')['Sales'].sum().idxmax() if not filtered_df.empty else "N/A"
        
        # Display KPIs in columns
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Total Sales", f"${total_sales:,.0f}")
        col2.metric("Total Profit", f"${total_profit:,.0f}")
        col3.metric("Number of Orders", f"{num_orders}")
        col4.metric("Growth Rate", f"{growth_rate:.1f}%")
        col5.metric("Top Region", f"{top_region}")
        col6.metric("Best Category", f"{best_category}")
        
        st.markdown("---")
        
        # Visualizations
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Monthly Sales Trend")
            monthly_trend = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
            monthly_trend['Order Date'] = monthly_trend['Order Date'].astype(str)
            
            fig1, ax1 = plt.subplots(figsize=(8, 4))
            ax1.plot(monthly_trend['Order Date'], monthly_trend['Sales'], marker='o', color='#2ca02c')
            plt.xticks(rotation=45)
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Sales ($)")
            ax1.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig1)

        with col_chart2:
            st.subheader("Sales by Region")
            region_sales = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            sns.barplot(data=region_sales, x='Region', y='Sales', palette='Blues_r', ax=ax2, hue='Region', legend=False)
            ax2.set_ylabel("Sales ($)")
            st.pyplot(fig2)
            
        st.markdown("---")
        
        col_chart3, col_chart4 = st.columns([1, 1])
        
        with col_chart3:
            st.subheader("Profit Distribution by Category")
            category_profit = filtered_df.groupby('Category')['Profit'].sum()
            fig3, ax3 = plt.subplots(figsize=(6, 6))
            ax3.pie(category_profit, labels=category_profit.index, autopct='%1.1f%%', 
                    startangle=90, colors=['#1f77b4', '#ff7f0e', '#2ca02c'],
                    explode=[0.05]*len(category_profit), shadow=True)
            st.pyplot(fig3)
            
        with col_chart4:
            st.subheader("Raw Data Snippet")
            st.dataframe(filtered_df[['Order Date', 'Customer Name', 'Region', 'Category', 'Sales', 'Profit']].head(15), use_container_width=True)
