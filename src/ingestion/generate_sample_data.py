"""
DataSentry - Sample Data Generator

Generates ~100k realistic transaction records with deliberately injected data-quality problems:
- NULL values
- Duplicates
- Invalid values
- Schema changes
- Missing records
- Abnormal revenue patterns
"""

import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
import numpy as np

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Configuration
NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_ORDERS = 100000
OUTPUT_DIR = "../../data"


def generate_customers(num_customers):
    """Generate customer data with some quality issues."""
    customers = []
    for i in range(num_customers):
        customer = {
            "id": str(uuid.uuid4()),
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "created_at": fake.date_time_between(start_date="-2y", end_date="now"),
            "status": random.choice(["active", "active", "active", "inactive", "suspended"])
        }
        customers.append(customer)
    
    # Inject NULL values (5% of customers missing phone)
    for customer in customers[:int(num_customers * 0.05)]:
        customer["phone"] = None
    
    # Inject duplicate emails (0.5%)
    if len(customers) > 10:
        duplicate_email = customers[0]["email"]
        customers[1]["email"] = duplicate_email
    
    return pd.DataFrame(customers)


def generate_products(num_products):
    """Generate product data with some quality issues."""
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
    products = []
    
    for i in range(num_products):
        product = {
            "id": str(uuid.uuid4()),
            "name": fake.word() + " " + fake.word(),
            "sku": f"SKU-{i:05d}",
            "category": random.choice(categories),
            "price": round(random.uniform(10.0, 500.0), 2),
            "stock_quantity": random.randint(0, 1000),
            "created_at": fake.date_time_between(start_date="-2y", end_date="now"),
            "status": random.choice(["available", "available", "available", "discontinued", "out_of_stock"])
        }
        products.append(product)
    
    # Inject negative prices (0.2% - invalid data)
    for product in products[:int(num_products * 0.002)]:
        product["price"] = -abs(product["price"])
    
    # Inject duplicate SKUs (0.5%)
    if len(products) > 10:
        duplicate_sku = products[0]["sku"]
        products[1]["sku"] = duplicate_sku
    
    return pd.DataFrame(products)


def generate_orders_and_payments(num_orders, customers_df, products_df):
    """Generate orders and payments with various data quality issues."""
    orders = []
    payments = []
    order_items = []
    
    customer_ids = customers_df["id"].tolist()
    product_ids = products_df["id"].tolist()
    product_prices = {row["id"]: row["price"] for _, row in products_df.iterrows()}
    
    # Generate orders over the past year
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(num_orders):
        order_date = start_date + timedelta(days=random.randint(0, 365))
        customer_id = random.choice(customer_ids)
        
        # Random number of items per order (1-5)
        num_items = random.randint(1, 5)
        selected_products = random.sample(product_ids, min(num_items, len(product_ids)))
        
        total_amount = 0.0
        for product_id in selected_products:
            quantity = random.randint(1, 3)
            unit_price = product_prices[product_id]
            item_total = quantity * unit_price
            total_amount += item_total
            
            order_items.append({
                "id": str(uuid.uuid4()),
                "order_id": None,  # Will be set after order creation
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "created_at": order_date
            })
        
        order = {
            "id": str(uuid.uuid4()),
            "customer_id": customer_id,
            "order_date": order_date,
            "total_amount": round(total_amount, 2),
            "status": random.choice(["pending", "confirmed", "shipped", "delivered", "cancelled", "refunded"]),
            "shipping_address": fake.address().replace("\n", ", "),
            "tracking_number": f"TRK-{random.randint(100000, 999999)}",
            "created_at": order_date
        }
        orders.append(order)
        
        # Link order items to this order
        for item in order_items[-num_items:]:
            item["order_id"] = order["id"]
        
        # Generate payment
        payment = {
            "id": str(uuid.uuid4()),
            "order_id": order["id"],
            "payment_date": order_date + timedelta(hours=random.randint(0, 48)),
            "amount": round(total_amount, 2),
            "payment_method": random.choice(["credit_card", "debit_card", "paypal", "bank_transfer", "crypto"]),
            "payment_status": random.choice(["completed", "completed", "completed", "pending", "failed", "refunded"]),
            "transaction_id": f"TXN-{random.randint(100000000, 999999999)}",
            "created_at": order_date
        }
        payments.append(payment)
    
    orders_df = pd.DataFrame(orders)
    payments_df = pd.DataFrame(payments)
    order_items_df = pd.DataFrame(order_items)
    
    # Inject data quality issues
    
    # 1. NULL payment_status (18.7% of payments - simulates API schema change)
    null_count = int(len(payments_df) * 0.187)
    null_indices = random.sample(range(len(payments_df)), null_count)
    payments_df.loc[null_indices, "payment_status"] = None
    
    # 2. NULL customer_id in orders (2% - orphaned orders)
    null_customer_count = int(len(orders_df) * 0.02)
    null_customer_indices = random.sample(range(len(orders_df)), null_customer_count)
    orders_df.loc[null_customer_indices, "customer_id"] = None
    
    # 3. Duplicate orders (1%)
    duplicate_count = int(len(orders_df) * 0.01)
    duplicates = orders_df.head(duplicate_count).copy()
    # Change IDs to make them new records but with same data
    duplicates["id"] = [str(uuid.uuid4()) for _ in range(duplicate_count)]
    orders_df = pd.concat([orders_df, duplicates], ignore_index=True)
    
    # 4. Abnormal revenue - inject orders with very high amounts (0.5%)
    high_revenue_count = int(len(orders_df) * 0.005)
    high_revenue_indices = random.sample(range(len(orders_df)), high_revenue_count)
    orders_df.loc[high_revenue_indices, "total_amount"] = orders_df.loc[high_revenue_indices, "total_amount"] * 100
    
    # 5. Missing products in order_items (referential integrity issue)
    # Remove some product_ids from products but keep them in order_items
    if len(order_items_df) > 0:
        orphaned_product_id = order_items_df.iloc[0]["product_id"]
        # Remove this product from products_df
        products_df = products_df[products_df["id"] != orphaned_product_id]
    
    # 6. Invalid status values (0.3%)
    invalid_status_count = int(len(orders_df) * 0.003)
    invalid_status_indices = random.sample(range(len(orders_df)), invalid_status_count)
    orders_df.loc[invalid_status_indices, "status"] = "invalid_status"
    
    # 7. Future dates (0.2%)
    future_date_count = int(len(orders_df) * 0.002)
    future_date_indices = random.sample(range(len(orders_df)), future_date_count)
    future_date = datetime.now() + timedelta(days=30)
    orders_df.loc[future_date_indices, "order_date"] = future_date
    
    return orders_df, payments_df, order_items_df, products_df


def main():
    """Main function to generate all sample data."""
    print("Generating sample data...")
    
    # Generate customers
    print(f"Generating {NUM_CUSTOMERS} customers...")
    customers_df = generate_customers(NUM_CUSTOMERS)
    
    # Generate products
    print(f"Generating {NUM_PRODUCTS} products...")
    products_df = generate_products(NUM_PRODUCTS)
    
    # Generate orders, payments, and order items
    print(f"Generating {NUM_ORDERS} orders with payments and items...")
    orders_df, payments_df, order_items_df, products_df = generate_orders_and_payments(
        NUM_ORDERS, customers_df, products_df
    )
    
    # Save to CSV files
    print("Saving data to CSV files...")
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    customers_df.to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)
    products_df.to_csv(f"{OUTPUT_DIR}/products.csv", index=False)
    orders_df.to_csv(f"{OUTPUT_DIR}/orders.csv", index=False)
    payments_df.to_csv(f"{OUTPUT_DIR}/payments.csv", index=False)
    order_items_df.to_csv(f"{OUTPUT_DIR}/order_items.csv", index=False)
    
    # Print statistics
    print("\n=== Data Generation Complete ===")
    print(f"Customers: {len(customers_df)}")
    print(f"Products: {len(products_df)}")
    print(f"Orders: {len(orders_df)}")
    print(f"Payments: {len(payments_df)}")
    print(f"Order Items: {len(order_items_df)}")
    
    print("\n=== Data Quality Issues Injected ===")
    print(f"NULL payment_status: {payments_df['payment_status'].isna().sum()} ({payments_df['payment_status'].isna().sum()/len(payments_df)*100:.1f}%)")
    print(f"NULL customer_id: {orders_df['customer_id'].isna().sum()} ({orders_df['customer_id'].isna().sum()/len(orders_df)*100:.1f}%)")
    print(f"Negative product prices: {(products_df['price'] < 0).sum()}")
    print(f"Invalid order statuses: {(orders_df['status'] == 'invalid_status').sum()}")
    print(f"Future order dates: {(orders_df['order_date'] > datetime.now()).sum()}")
    print(f"Duplicate customer emails: {customers_df['email'].duplicated().sum()}")
    print(f"Duplicate product SKUs: {products_df['sku'].duplicated().sum()}")
    
    print(f"\nData saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
