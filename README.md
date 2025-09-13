# ☕ Coffee Shop API

A FastAPI application for ordering delicious coffee with comprehensive options and validation.

## Features

- **Complete Coffee Menu**: Multiple sizes, types, flavors, and milk options
- **Smart Pricing**: Automatic price calculation based on selections
- **Order Management**: Create, view, update, and cancel orders
- **Input Validation**: Comprehensive validation for all order parameters
- **Interactive Documentation**: Auto-generated API docs with Swagger UI
- **Order Tracking**: Status updates and estimated preparation times

## Available Options

### Sizes
- Small ($3.50)
- Medium ($4.25)  
- Large ($4.95)

### Coffee Types
- Hot
- Iced (+$1.00 prep time)

### Flavors (+$0.50 each, max 3)
- French Vanilla
- Hazelnut
- Caramel
- Mocha
- Vanilla
- Cinnamon

### Milk Options
- Whole (included)
- None (included)
- Oat (+$0.65)
- Almond (+$0.65)
- Soy (+$0.65)

### Extras
- Extra Espresso Shots (+$0.75 each, max 5)
- Special Instructions (up to 200 characters)

## Quick Start

1. **Install dependencies**:
   ```bash
   uv add fastapi uvicorn httpx
   ```

2. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Endpoints

### General
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /menu` - Get complete menu options

### Orders
- `POST /orders` - Create a new coffee order
- `GET /orders` - Get all orders
- `GET /orders/{order_id}` - Get specific order
- `PATCH /orders/{order_id}/status` - Update order status
- `DELETE /orders/{order_id}` - Cancel order

## Example Usage

### Simple Order
```json
{
  "size": "medium",
  "coffee_type": "hot"
}
```

### Complex Order
```json
{
  "size": "large",
  "coffee_type": "iced",
  "flavors": ["hazelnut", "caramel"],
  "milk": "oat",
  "extra_shot": 2,
  "special_instructions": "Extra hot, light foam"
}
```

### Response Example
```json
{
  "order_id": "123e4567-e89b-12d3-a456-426614174000",
  "size": "large",
  "coffee_type": "iced",
  "flavors": ["hazelnut", "caramel"],
  "milk": "oat",
  "extra_shot": 2,
  "special_instructions": "Extra hot, light foam",
  "estimated_price": 7.85,
  "estimated_prep_time": 5,
  "order_time": "2025-09-13T10:30:00",
  "status": "received"
}
```

## Testing the API

Run the example script to test all endpoints:

```bash
python example_usage.py
```

## Validation Rules

- **Flavors**: Maximum 3 flavors per order
- **Extra Shots**: 0-5 shots allowed
- **Special Instructions**: Maximum 200 characters
- **Order Cancellation**: Cannot cancel orders that are "ready" or "completed"

## Development

The application uses:
- **FastAPI** for the web framework
- **Pydantic** for data validation and serialization
- **Uvicorn** as the ASGI server
- **UUID** for unique order identification
- **In-memory storage** (replace with database for production)

## Project Structure

```
coffee_shop/
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic models and enums
├── example_usage.py     # Example API usage script
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```
