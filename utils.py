"""Utility functions for the logistics analytics dashboard."""
import os
import pandas as pd
from typing import Dict, Optional, Any
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data() -> Optional[Dict[str, pd.DataFrame]]:
    """
    Load all data files from the data directory.
    
    Returns:
        Dict[str, pd.DataFrame]: Dictionary mapping dataset names to DataFrames
        None: If an error occurs during loading
    """
    from config import DATA_DIR, DATA_FILES
    
    data = {}
    try:
        for name, filename in DATA_FILES.items():
            filepath = os.path.join(DATA_DIR, filename)
            if not os.path.exists(filepath):
                logger.warning(f"File not found: {filepath}")
                continue
                
            df = pd.read_csv(filepath)
            # Convert column names to lowercase for consistency
            df.columns = df.columns.str.lower()
            data[name] = df
            logger.info(f"Loaded {len(df)} rows from {filename}")
            
        return data if data else None
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return None

def calculate_inventory_metrics(warehouse_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate key inventory metrics.
    
    Args:
        warehouse_df: DataFrame containing warehouse inventory data
        
    Returns:
        Dict containing calculated metrics
    """
    if warehouse_df.empty:
        return {}
        
    return {
        'total_products': len(warehouse_df['product_category'].unique()),
        'total_warehouses': len(warehouse_df['location'].unique()),
        'total_inventory': int(warehouse_df['current_stock_units'].sum()),
        'avg_stock_level': float(warehouse_df['current_stock_units'].mean()),
        'low_stock_items': int((warehouse_df['current_stock_units'] < warehouse_df['reorder_level']).sum())
    }

def generate_rebalancing_suggestions(inventory_status: pd.DataFrame) -> pd.DataFrame:
    """
    Generate inventory rebalancing suggestions based on inventory status.
    
    Args:
        inventory_status: DataFrame with inventory status (demand, current_stock_units, variance)
        
    Returns:
        DataFrame with rebalancing suggestions
    """
    from config import REBALANCE_THRESHOLD
    
    rebalance = inventory_status[
        (inventory_status['variance'].abs() > REBALANCE_THRESHOLD)
    ].copy()
    
    if not rebalance.empty:
        rebalance['action'] = rebalance['variance'].apply(
            lambda x: 'Increase Stock' if x < 0 else 'Reduce Stock'
        )
        rebalance['quantity'] = rebalance['variance'].abs()
    
    return rebalance

def get_surplus_warehouses(warehouse_df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    Find warehouses with surplus stock for a given product category.
    
    Args:
        warehouse_df: DataFrame with warehouse inventory data
        category: Product category to check
        
    Returns:
        DataFrame of warehouses with surplus stock
    """
    from config import SURPLUS_THRESHOLD
    
    return warehouse_df[
        (warehouse_df['product_category'] == category) &
        (warehouse_df['current_stock_units'] > warehouse_df['reorder_level'] * SURPLUS_THRESHOLD)
    ]
