import streamlit as st
import pandas as pd
import os
from pathlib import Path

# Set page config (must be the first Streamlit command)
st.set_page_config(
    page_title="NexGen Logistics Analytics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data():
    """Load and cache the dataset."""
    data_dir = Path("data")
    
    # List of expected CSV files
    csv_files = [
        'orders.csv',
        'delivery_performance.csv',
        'routes_distance.csv',
        'vehicle_fleet.csv',
        'warehouse_inventory.csv',
        'customer_feedback.csv',
        'cost_breakdown.csv'
    ]
    
    data = {}
    for name, df in data.items():
        dataset_info.append({
            "Dataset": name,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Values": df.isnull().sum().sum(),
            "Size (MB)": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
        })
    
    # Display the dataset information
    st.dataframe(
        pd.DataFrame(dataset_info).sort_values("Rows", ascending=False),
        use_container_width=True,
        hide_index=True
    )

def explore_dataset(data: Dict[str, pd.DataFrame], dataset_name: str) -> None:
    """Allow exploration of a specific dataset."""
    st.subheader(f"🔍 Exploring: {dataset_name}")
    df = data[dataset_name]
    
    # Display basic information
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    
    # Tabs for different exploration options
    tab1, tab2, tab3 = st.tabs(["📋 Data Preview", "ℹ️ Column Info", "📈 Statistics"])
    
    with tab1:
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        # Get column information
        col_info = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str),
            "Missing %": (df.isnull().mean() * 100).round(2)
        })
        st.dataframe(col_info, use_container_width=True, hide_index=True)
    
    with tab3:
        # Display statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.subheader("Numeric Columns Statistics")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        
        # Display value counts for categorical columns
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(cat_cols) > 0:
            st.subheader("Categorical Columns Value Counts")
            for col in cat_cols:
                st.write(f"**{col}**")
                st.dataframe(df[col].value_counts().reset_index().rename(
                    columns={"index": "Value", col: "Count"}
                ), use_container_width=True, hide_index=True)

def optimize_warehouse_inventory(data: Dict[str, pd.DataFrame]) -> None:
    """Optimize warehouse inventory levels based on demand."""
    try:
        st.header("🏭 Warehouse Optimization Tool")
        
        # Get warehouse and product data
        warehouse_df = data.get('warehouse_inventory')
        orders_df = data.get('orders')
        
        if warehouse_df is None or orders_df is None:
            st.error("❌ Required datasets not found.")
            return
            
        # Convert column names to lowercase for consistency
        orders_df.columns = orders_df.columns.str.lower()
        warehouse_df.columns = warehouse_df.columns.str.lower()
        
        # Display current inventory metrics
        st.subheader("📊 Inventory Metrics")
        metrics = calculate_inventory_metrics(warehouse_df)
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Products", metrics['total_products'])
            col2.metric("Total Warehouses", metrics['total_warehouses'])
            col3.metric("Total Inventory", f"{metrics['total_inventory']:,}")
            col4.metric("Low Stock Items", metrics['low_stock_items'])
        
        # Calculate demand by product category
        demand = orders_df.groupby('product_category').size().reset_index(name='demand')
        
        # Calculate current inventory by product category
        inventory = warehouse_df.groupby('product_category')['current_stock_units'].sum().reset_index()
        
        # Merge demand and inventory
        inventory_status = pd.merge(demand, inventory, on='product_category', how='outer').fillna(0)
        inventory_status['variance'] = inventory_status['current_stock_units'] - inventory_status['demand']
        
        # Display inventory vs demand analysis
        st.subheader("📈 Inventory vs Demand Analysis")
        st.dataframe(inventory_status, use_container_width=True)
        
        # Generate rebalancing suggestions
        st.subheader("🔄 Rebalancing Recommendations")
        rebalance = generate_rebalancing_suggestions(inventory_status)
        
        if len(rebalance) == 0:
            st.success("✅ Inventory levels are well-balanced across all product categories.")
        else:
            # Display the rebalance recommendations
            st.dataframe(
                rebalance[['product_category', 'action', 'quantity']],
                use_container_width=True
            )
            
            # Generate rebalancing plan
            st.subheader("📋 Rebalancing Plan")
            for _, row in rebalance.iterrows():
                category = row['product_category']
                quantity = int(row['quantity'])
                action = row['action']
                
                st.write(f"### {category}")
                st.write(f"**Action:** {action} by {quantity} units")
                
                if action == 'Increase Stock':
                    st.write("#### Potential Source Warehouses")
                    surplus_warehouses = get_surplus_warehouses(warehouse_df, category)
                    
                    if not surplus_warehouses.empty:
                        for _, wh in surplus_warehouses.iterrows():
                            available = int(wh['current_stock_units'] - wh['reorder_level'])
                            st.write(f"- **{wh['location']}**: Can provide up to {available} units")
                    else:
                        st.warning("No surplus inventory found. Consider new procurement.")
                
                st.write("---")
                
    except Exception as e:
        logger.error(f"Error in warehouse optimization: {e}")
        st.error(f"An error occurred: {str(e)}")

def main() -> None:
    """Main function to run the Streamlit app."""
    st.title("🚚 NexGen Logistics Analytics")
    st.markdown("""
    Welcome to the NexGen Logistics Analytics Dashboard. This tool helps analyze and optimize logistics operations.
    """)
    
    # Load data
    with st.spinner('🔍 Loading data...'):
        data = load_data()
    
    if not data:
        st.error("❌ Failed to load data. Please check the 'data' directory and try again.")
        return
    
    # Sidebar with dataset selection
    st.sidebar.header("📂 Datasets")
    dataset_name = st.sidebar.selectbox(
        "Select a dataset:",
        list(data.keys()),
        index=0
    )
    
    # Display dataset metrics in sidebar
    st.sidebar.metric("Total Datasets", len(data))
    st.sidebar.metric("Total Rows", f"{len(data[dataset_name]):,}")
    st.sidebar.metric("Total Columns", len(data[dataset_name].columns))
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Explore", "🏭 Warehouse Optimization"])
    
    with tab1:
        display_dataset_overview(data)
    
    with tab2:
        explore_dataset(data, dataset_name)
    
    with tab3:
        optimize_warehouse_inventory(data)
    
    # Add a footer
    st.markdown("---")
    st.caption("© 2025 NexGen Logistics Analytics | Built with Streamlit")

if __name__ == "__main__":
    main()
