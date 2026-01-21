from typing import List, Dict

# Mock Database
PRODUCTS = [
    {"id": 1, "name": "Enterprise Plan", "tags": ["contract", "price", "budget", "enterprise"], "description": "Full access to all features with dedicated support."},
    {"id": 2, "name": "Startup Pack", "tags": ["discount", "startup", "price", "budget"], "description": "Discounted rate for early-stage companies."},
    {"id": 3, "name": "Competitor Switcher", "tags": ["competitor", "switch"], "description": "Special offer for customers switching from other vendors."},
    {"id": 4, "name": "Annual Billing", "tags": ["contract", "billing", "year"], "description": "Save 20% with annual billing."},
    {"id": 5, "name": "Universal Laptop Charger", "tags": ["charger", "laptop", "power", "hardware"], "description": "90W Universal charger compatible with most laptops."},
    {"id": 6, "name": "MacBook Pro Charger", "tags": ["charger", "macbook", "magsafe", "power"], "description": "Apple 96W USB-C Power Adapter."},
]

CUSTOMERS = {
    "1": {"name": "Acme Corp", "history": ["bought_basic"], "segment": "enterprise"},
    "2": {"name": "TechStart Inc", "history": [], "segment": "startup"}
}

def get_product_recommendations(keywords: List[str], customer_id: str = None) -> List[Dict]:
    """
    Returns product recommendations based on conversation keywords and (optional) customer profile.
    """
    recommendations = []
    
    # Keyword-based matching
    for product in PRODUCTS:
        # If any keyword matches the product tags
        if any(k in product["tags"] for k in keywords):
            recommendations.append(product)
            
    # Customer Segment matching (Mock logic)
    if customer_id and customer_id in CUSTOMERS:
        customer = CUSTOMERS[customer_id]
        if customer["segment"] == "startup":
             recommendations.append(PRODUCTS[1]) # Suggest Startup Pack
             
    # Deduplicate by ID
    unique_recs = {r["id"]: r for r in recommendations}.values()
    return list(unique_recs)
