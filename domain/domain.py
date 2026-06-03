from pydantic import BaseModel, Field

class InventoryRequest(BaseModel):
    sku_number: int = Field(
        ...,
        ge=1,
        le=300,
        description="SKU number between 1 and 300"
    )

    lead_time: float = Field(ge=7,le=30)
    service_level: float = Field(ge=50.0, le=99.99)
    holding_cost: float = Field(ge=1, le=100)
    order_cost: float = Field(ge=10, le=10000)


class InventoryResponse(BaseModel):
    sku_id: str
    avg_daily_demand: float
    demand_std: float
    safety_stock: float
    reorder_point: float
    eoq: float


class WarehouseRiskResponse(BaseModel):
    warehouse: str
    risk_pct: float


class ForecastResponse(BaseModel):
    date: str
    forecast: float
    lower_bound: float
    upper_bound: float