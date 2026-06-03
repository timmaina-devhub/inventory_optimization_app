from fastapi import FastAPI, HTTPException

from domain.domain import (
    InventoryRequest,
    InventoryResponse
)

from service.inventory_service import (
    calculate_inventory,
    get_forecast,
    get_skus,
    get_sku_details,
    get_warehouse_risk
)

inventory_app = FastAPI(
    title="Inventory Optimization API",
    description="""
    Supply Chain Analytics API

    Features:
    - Inventory Optimization
    - Warehouse Risk Monitoring
    - Demand Forecast Retrieval
    - SKU Analytics
    """,
    version="1.0.0"
)


@inventory_app.get("/")
def root():

    return {
        "message":
        "Inventory Optimization API Running"
    }


# SKU LIST

@inventory_app.get("/skus")
def skus():

    return {
        "skus": get_skus()
    }



# SKU DETAILS

@inventory_app.get("/sku/{sku_id}")
def sku_details(
    sku_id: str
):

    try:

        return get_sku_details(
            sku_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
        

# FORECAST

@inventory_app.get("/forecast")
def forecast():

    return get_forecast()


# WAREHOUSE RISK


@inventory_app.get("/warehouse-risk")
def warehouse_risk():

    return get_warehouse_risk()




# INVENTORY OPTIMIZATION

@inventory_app.post(
    "/inventory/calculate",
    response_model=InventoryResponse
)
def inventory_calculation(
    request: InventoryRequest
):

    try:

        return calculate_inventory(
            sku_number=request.sku_number,
            lead_time=request.lead_time,
            service_level=request.service_level,
            holding_cost=request.holding_cost,
            order_cost=request.order_cost
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )