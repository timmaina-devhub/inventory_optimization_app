import numpy as np
import pandas as pd

from scipy.stats import norm


# DATA LOADING


SKU_STATS_PATH = "artifacts/sku_stats.parquet"
WAREHOUSE_RISK_PATH = "artifacts/warehouse_risk.parquet"
FORECAST_PATH = "artifacts/forecast.parquet"
INVENTORY_PATH = "artifacts/inventory.parquet"


sku_stats = pd.read_parquet(SKU_STATS_PATH)
warehouse_risk = pd.read_parquet(WAREHOUSE_RISK_PATH)
forecast_df = pd.read_parquet(FORECAST_PATH)
inventory_df = pd.read_parquet(INVENTORY_PATH)


 
# HELPERS


def build_sku_id(sku_number: int) -> str:
    """
    Convert:
        1   -> SKU0001
        25  -> SKU0025
        300 -> SKU0300
    """
    return f"SKU{sku_number:04d}"


def get_sku_row(sku_number: int) -> pd.Series:
    """
    Retrieve a SKU record from sku_stats.
    """

    sku_id = build_sku_id(sku_number)

    sku_row = sku_stats.loc[
        sku_stats["sku_id"] == sku_id
    ]

    if sku_row.empty:
        raise ValueError(f"SKU '{sku_id}' not found.")

    return sku_row.iloc[0]



# INVENTORY OPTIMIZATION

def calculate_inventory(
    sku_number: int,
    lead_time: float,
    service_level: float,
    holding_cost: float,
    order_cost: float
) -> dict:

    sku = get_sku_row(sku_number)

    sku_id = sku["sku_id"]

    avg_daily_demand = float(
        sku["avg_daily_demand"]
    )

    demand_std = float(
        sku["demand_std"]
    )

    z_score = norm.ppf(
        service_level / 100
    )

    safety_stock = (
        z_score
        * demand_std
        * np.sqrt(lead_time)
    )

    reorder_point = (
        avg_daily_demand * lead_time
    ) + safety_stock

    annual_demand = (
        avg_daily_demand * 365
    )

    eoq = np.sqrt(
        (
            2
            * annual_demand
            * order_cost
        ) / holding_cost
    )

    return {
        "sku_id": sku_id,
        "avg_daily_demand": round(avg_daily_demand, 2),
        "demand_std": round(demand_std, 2),
        "safety_stock": round(float(safety_stock), 2),
        "reorder_point": round(float(reorder_point), 2),
        "eoq": round(float(eoq), 2),
    }


# SKU LIST

def get_skus() -> list[str]:

    return sorted(
        sku_stats["sku_id"]
        .astype(str)
        .unique()
        .tolist()
    )


# WAREHOUSE RISK

def get_warehouse_risk() -> list[dict]:

    return warehouse_risk.to_dict(
        orient="records"
    )


# FORECAST

def get_forecast() -> list[dict]:

    forecast = forecast_df.copy()

    forecast["date"] = (
        forecast["date"]
        .astype(str)
    )

    return forecast.to_dict(
        orient="records"
    )



# SKU DETAILS

def get_sku_details(
    sku_number: int
) -> dict:

    sku_id = build_sku_id(sku_number)

    sku = get_sku_row(sku_number)

    inventory_rows = inventory_df.loc[
        inventory_df["sku_id"] == sku_id
    ]

    current_stock = int(
        inventory_rows["closing_stock"].sum()
    )

    stockout_count = int(
        inventory_rows["stockout_flag"].sum()
    )

    return {
        "sku_id": sku_id,
        "avg_daily_demand": float(
            sku["avg_daily_demand"]
        ),
        "demand_std": float(
            sku["demand_std"]
        ),
        "current_stock": current_stock,
        "stockout_count": stockout_count,
    }