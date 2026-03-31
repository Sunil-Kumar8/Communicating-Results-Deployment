import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set plot style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

def generate_sample_data(num_records=1000):
    np.random.seed(42)
    
    # Generate dates over the last year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(num_records)]
    
    regions = ['North', 'South', 'East', 'West']
    categories = ['Technology', 'Furniture', 'Office Supplies']
    
    data = {
        'Order Date': dates,
        'Customer Name': [f'Customer_{i}' for i in np.random.randint(1, 500, num_records)],
        'Region': np.random.choice(regions, num_records, p=[0.2, 0.25, 0.2, 0.35]),
        'Category': np.random.choice(categories, num_records, p=[0.4, 0.3, 0.3]),
        'Sales': np.random.uniform(50, 2000, num_records),
    }
    
    df = pd.DataFrame(data)
    
    # Add profit based on category margins
    margins = {'Technology': 0.25, 'Furniture': 0.15, 'Office Supplies': 0.30}
    df['Profit'] = df.apply(lambda row: row['Sales'] * margins[row['Category']] * np.random.uniform(0.8, 1.2), axis=1)
    
    # Sort by date
    df = df.sort_values('Order Date').reset_index(drop=True)
    return df

def calculate_kpis(df):
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    num_orders = len(df)
    
    # Monthly growth rate
    df['Month'] = df['Order Date'].dt.to_period('M')
    monthly_sales = df.groupby('Month')['Sales'].sum()
    if len(monthly_sales) > 1:
        growth_rate = ((monthly_sales.iloc[-1] - monthly_sales.iloc[-2]) / monthly_sales.iloc[-2]) * 100
    else:
        growth_rate = 0
        
    top_region = df.groupby('Region')['Sales'].sum().idxmax()
    best_category = df.groupby('Category')['Sales'].sum().idxmax()
    
    print("-" * 50)
    print("KEY PERFORMANCE INDICATORS (KPIs)")
    print("-" * 50)
    print(f"Total Sales:          ${total_sales:,.2f}")
    print(f"Total Profit:         ${total_profit:,.2f}")
    print(f"Number of Orders:     {num_orders}")
    print(f"Monthly Growth Rate:  {growth_rate:,.2f}%")
    print(f"Top Performing Region: {top_region}")
    print(f"Best Selling Category: {best_category}")
    print("-" * 50)

def visualize_data(df):
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Business Analytics Dashboard', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Line chart for sales trend over time
    ax1 = plt.subplot(2, 2, (1, 2))
    monthly_trend = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly_trend['Order Date'] = monthly_trend['Order Date'].dt.to_timestamp()
    
    ax1.plot(monthly_trend['Order Date'], monthly_trend['Sales'], marker='o', linewidth=2, color='#2ca02c')
    ax1.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Total Sales ($)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 2. Bar chart for sales by region
    ax2 = plt.subplot(2, 2, 3)
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    sns.barplot(x=region_sales.index, y=region_sales.values, ax=ax2, palette='Blues_r', hue=region_sales.index, legend=False)
    ax2.set_title('Sales by Region', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Total Sales ($)')
    
    # 3. Pie chart for category distribution based on Profit
    ax3 = plt.subplot(2, 2, 4)
    category_profit = df.groupby('Category')['Profit'].sum()
    ax3.pie(category_profit, labels=category_profit.index, autopct='%1.1f%%', 
            startangle=90, colors=['#1f77b4', '#ff7f0e', '#2ca02c'],
            explode=(0.05, 0.05, 0.05), shadow=True)
    ax3.set_title('Profit Distribution by Category', fontsize=14, fontweight='bold')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save the dashboard
    plt.savefig('dashboard_visualization.png', dpi=300, bbox_inches='tight')
    print("\n-> Dashboard visualization saved as 'dashboard_visualization.png'")
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    print('Generating e-commerce dataset...')
    df = generate_sample_data(2000)
    
    # Save dataset to CSV
    df.drop('Month', axis=1, errors='ignore').to_csv('ecommerce_sales_data.csv', index=False)
    print("-> Dataset saved as 'ecommerce_sales_data.csv'")
    
    # Calculate and display KPIs
    calculate_kpis(df)
    
    # Generate Visualizations
    visualize_data(df)
