from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import (
    CoffeeOrder, 
    CoffeeOrderResponse, 
    OrderStatus, 
    MenuResponse,
    SizeEnum,
    CoffeeTypeEnum,
    FlavorEnum,
    MilkTypeEnum
)
import uuid
from datetime import datetime, timedelta
from typing import Dict, List
import uvicorn

app = FastAPI(
    title="Coffee Shop API",
    description="A FastAPI application for ordering delicious coffee ☕",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# In-memory storage for orders (in production, use a proper database)
orders_db: Dict[str, CoffeeOrderResponse] = {}

# Pricing configuration
PRICING = {
    "base_prices": {
        SizeEnum.SMALL: 3.50,
        SizeEnum.MEDIUM: 4.25,
        SizeEnum.LARGE: 4.95
    },
    "extra_shot": 0.75,
    "flavor": 0.50,
    "premium_milk": 0.65  # for oat, almond, soy
}

def calculate_price(order: CoffeeOrder) -> float:
    """Calculate the total price for a coffee order."""
    base_price = PRICING["base_prices"][order.size]
    
    # Add extra shots
    if order.extra_shot:
        base_price += order.extra_shot * PRICING["extra_shot"]
    
    # Add flavors
    base_price += len(order.flavors) * PRICING["flavor"]
    
    # Add premium milk upcharge
    if order.milk and order.milk in [MilkTypeEnum.OAT, MilkTypeEnum.ALMOND, MilkTypeEnum.SOY]:
        base_price += PRICING["premium_milk"]
    
    return round(base_price, 2)

def calculate_prep_time(order: CoffeeOrder) -> int:
    """Calculate estimated preparation time in minutes."""
    base_time = 3  # Base prep time
    
    # Add time for extra complexity
    if order.coffee_type == CoffeeTypeEnum.ICED:
        base_time += 1
    
    if order.extra_shot:
        base_time += order.extra_shot * 0.5
    
    if len(order.flavors) > 1:
        base_time += 1
    
    return max(2, int(base_time))  # Minimum 2 minutes

@app.get("/", tags=["General"])
async def root():
    """Welcome message for the Coffee Shop API."""
    return {
        "message": "Welcome to the Coffee Shop API! ☕", 
        "docs": "/docs",
        "menu": "/menu"
    }

@app.get("/menu", response_model=MenuResponse, tags=["Menu"])
async def get_menu():
    """Get the complete coffee menu with all available options."""
    return MenuResponse(
        sizes=[size.value for size in SizeEnum],
        coffee_types=[coffee_type.value for coffee_type in CoffeeTypeEnum],
        flavors=[flavor.value for flavor in FlavorEnum],
        milk_types=[milk.value for milk in MilkTypeEnum]
    )

@app.post("/orders", response_model=CoffeeOrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def create_coffee_order(order: CoffeeOrder):
    """Create a new coffee order."""
    try:
        order_id = str(uuid.uuid4())
        estimated_price = calculate_price(order)
        estimated_prep_time = calculate_prep_time(order)
        
        order_response = CoffeeOrderResponse(
            order_id=order_id,
            size=order.size,
            coffee_type=order.coffee_type,
            flavors=order.flavors,
            milk=order.milk,
            extra_shot=order.extra_shot,
            special_instructions=order.special_instructions,
            estimated_price=estimated_price,
            estimated_prep_time=estimated_prep_time,
            order_time=datetime.now(),
            status="received"
        )
        
        # Store order in memory
        orders_db[order_id] = order_response
        
        return order_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating order: {str(e)}"
        )

@app.get("/orders", response_model=List[CoffeeOrderResponse], tags=["Orders"])
async def get_all_orders():
    """Get all coffee orders."""
    return list(orders_db.values())

@app.get("/orders/{order_id}", response_model=CoffeeOrderResponse, tags=["Orders"])
async def get_order(order_id: str):
    """Get a specific coffee order by ID."""
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    return orders_db[order_id]

@app.patch("/orders/{order_id}/status", response_model=OrderStatus, tags=["Orders"])
async def update_order_status(order_id: str, status_update: OrderStatus):
    """Update the status of a coffee order."""
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    
    order = orders_db[order_id]
    order.status = status_update.status
    
    # Calculate estimated ready time based on status
    if status_update.status == "preparing":
        estimated_ready_time = datetime.now() + timedelta(minutes=order.estimated_prep_time)
    else:
        estimated_ready_time = None
    
    return OrderStatus(
        order_id=order_id,
        status=status_update.status,
        estimated_ready_time=estimated_ready_time
    )

@app.delete("/orders/{order_id}", tags=["Orders"])
async def cancel_order(order_id: str):
    """Cancel a coffee order."""
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    
    order = orders_db[order_id]
    if order.status in ["ready", "completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel order that is ready or completed"
        )
    
    del orders_db[order_id]
    return {"message": f"Order {order_id} has been cancelled"}

@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_orders": len(orders_db)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
