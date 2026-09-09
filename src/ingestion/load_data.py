"""
DataSentry - Data Loading Script

Loads generated CSV data into PostgreSQL database.
"""

import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "datasentry"),
    "user": os.getenv("DB_USER", "datasentry_user"),
    "password": os.getenv("DB_PASSWORD", "datasentry_pass")
}

DATA_DIR = "../../data"


def get_connection():
    """Create a database connection."""
    return psycopg2.connect(**DB_CONFIG)


def load_csv_to_table(csv_file, table_name, connection):
    """Load CSV data into a PostgreSQL table."""
    df = pd.read_csv(csv_file)
    
    cursor = connection.cursor()
    
    # Get column names from DataFrame
    columns = df.columns.tolist()
    
    # Prepare INSERT statement
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(map(sql.Identifier, columns)),
        sql.SQL(", ").join([sql.Placeholder()] * len(columns))
    )
    
    # Insert data
    inserted_count = 0
    for _, row in df.iterrows():
        # Convert NaN to None for NULL values
        values = [None if pd.isna(val) else val for val in row]
        
        # Handle UUID conversion if needed
        if 'id' in columns:
            idx = columns.index('id')
            if isinstance(values[idx], str):
                try:
                    values[idx] = uuid.UUID(values[idx])
                except ValueError:
                    pass  # Keep as string if not a valid UUID
        
        try:
            cursor.execute(insert_query, values)
            inserted_count += 1
        except Exception as e:
            print(f"Error inserting row into {table_name}: {e}")
            print(f"Row data: {values}")
    
    connection.commit()
    cursor.close()
    
    print(f"Inserted {inserted_count} rows into {table_name}")
    return inserted_count


def main():
    """Main function to load all data."""
    print("Connecting to database...")
    
    try:
        connection = get_connection()
        print("Connected successfully!")
        
        # Load data in correct order (respecting foreign keys)
        tables = [
            ("customers.csv", "customers"),
            ("products.csv", "products"),
            ("orders.csv", "orders"),
            ("payments.csv", "payments"),
            ("order_items.csv", "order_items")
        ]
        
        total_inserted = 0
        for csv_file, table_name in tables:
            csv_path = os.path.join(DATA_DIR, csv_file)
            if os.path.exists(csv_path):
                print(f"\nLoading {csv_file} into {table_name}...")
                count = load_csv_to_table(csv_path, table_name, connection)
                total_inserted += count
            else:
                print(f"Warning: {csv_path} not found. Skipping.")
        
        print(f"\n=== Data Loading Complete ===")
        print(f"Total rows inserted: {total_inserted}")
        
        connection.close()
        
    except Exception as e:
        print(f"Error: {e}")
        if 'connection' in locals():
            connection.close()


if __name__ == "__main__":
    main()
