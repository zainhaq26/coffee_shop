#!/usr/bin/env python3
"""
Example usage of the Coffee Shop API
Run this script after starting the server to see the API in action.
"""

import httpx
import json
from datetime import datetime

# API base URL (adjust if running on different host/port)
BASE_URL = "http://localhost:8000"

def print_response(title: str, response):
    """Helper function to print API responses nicely"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    if response.headers.get('content-type', '').startswith('application/json'):
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")

def main():
    print("Coffee Shop API Example Usage")
    print("Make sure the server is running with: uvicorn main:app --reload")
    
    with httpx.Client() as client:
        try:
            # 1. Check API health
            response = client.get(f"{BASE_URL}/health")
            print_response("Health Check", response)
            
            # 2. Get the menu
            response = client.get(f"{BASE_URL}/menu")
            print_response("Menu", response)
            
            # 3. Create a simple coffee order
            simple_order = {
                "size": "medium",
                "coffee_type": "hot"
            }
            response = client.post(f"{BASE_URL}/orders", json=simple_order)
            print_response("Simple Coffee Order", response)
            
            if response.status_code == 201:
                simple_order_id = response.json()["order_id"]
            
            # 4. Create a complex coffee order
            complex_order = {
                "size": "large",
                "coffee_type": "iced",
                "flavors": ["hazelnut", "caramel"],
                "milk": "oat",
                "extra_shot": 2,
                "special_instructions": "Extra hot, light foam"
            }
            response = client.post(f"{BASE_URL}/orders", json=complex_order)
            print_response("Complex Coffee Order", response)
            
            if response.status_code == 201:
                complex_order_id = response.json()["order_id"]
            
            # 5. Get all orders
            response = client.get(f"{BASE_URL}/orders")
            print_response("All Orders", response)
            
            # 6. Get a specific order
            if 'simple_order_id' in locals():
                response = client.get(f"{BASE_URL}/orders/{simple_order_id}")
                print_response("Get Specific Order", response)
                
                # 7. Update order status
                status_update = {
                    "order_id": simple_order_id,
                    "status": "preparing"
                }
                response = client.patch(f"{BASE_URL}/orders/{simple_order_id}/status", json=status_update)
                print_response("Update Order Status", response)
            
            # 8. Try to create an invalid order (too many flavors)
            invalid_order = {
                "size": "small",
                "coffee_type": "hot",
                "flavors": ["french vanilla", "hazelnut", "caramel", "mocha"]  # Too many flavors
            }
            response = client.post(f"{BASE_URL}/orders", json=invalid_order)
            print_response("Invalid Order (Too Many Flavors)", response)
            
            # 9. Try to create an invalid order (negative extra shots)
            invalid_order2 = {
                "size": "medium",
                "coffee_type": "iced",
                "extra_shot": -1  # Invalid negative value
            }
            response = client.post(f"{BASE_URL}/orders", json=invalid_order2)
            print_response("Invalid Order (Negative Extra Shots)", response)
            
            print(f"\n{'='*50}")
            print("Example completed! Check the API docs at http://localhost:8000/docs")
            print(f"{'='*50}")
            
        except httpx.ConnectError:
            print("\n❌ Error: Could not connect to the API server.")
            print("Make sure the server is running with: uvicorn main:app --reload")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
