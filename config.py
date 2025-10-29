"""Configuration and constants for the logistics analytics dashboard."""

# Data file paths
DATA_DIR = "data/"
DATA_FILES = {
    'orders': 'orders.csv',
    'warehouse_inventory': 'warehouse_inventory.csv',
    'delivery_performance': 'delivery_performance.csv',
    'routes_distance': 'routes_distance.csv',
    'vehicle_fleet': 'vehicle_fleet.csv',
    'customer_feedback': 'customer_feedback.csv',
    'cost_breakdown': 'cost_breakdown.csv'
}

# Rebalancing thresholds
REBALANCE_THRESHOLD = 5  # Minimum variance to trigger rebalancing
SURPLUS_THRESHOLD = 1.5  # Multiplier of reorder level to consider as surplus
