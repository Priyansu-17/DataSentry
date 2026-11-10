from fastapi import FastAPI, HTTPException
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DSN = (
    f"host={os.getenv('DB_HOST', 'localhost')} "
    f"port={os.getenv('DB_PORT', '5432')} "
    f"dbname={os.getenv('DB_NAME', 'datasentry')} "
    f"user={os.getenv('DB_USER', 'datasentry_user')} "
    f"password={os.getenv('DB_PASSWORD', 'datasentry_pass')}"
)

app = FastAPI(title="DataSentry API", version="0.1.0")

@app.get("/customers")
def list_customers(limit: int = 10):
    """Return a slice of customers for quick API testing."""
    with psycopg2.connect(DSN, cursor_factory=RealDictCursor) as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, email, first_name, last_name FROM customers LIMIT %s", (limit,)
        )
        rows = cur.fetchall()
    return {"customers": rows}

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """Fetch a single order together with its order items."""
    with psycopg2.connect(DSN, cursor_factory=RealDictCursor) as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT o.*, i.product_id, i.quantity, i.unit_price
            FROM orders o
            LEFT JOIN order_items i ON i.order_id = o.id
            WHERE o.id = %s
            """,
            (order_id,)
        )
        rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Order not found")
    # First row holds order fields; the rest are items
    order = dict(rows[0])
    order["items"] = [
        {"product_id": r["product_id"], "quantity": r["quantity"], "unit_price": r["unit_price"]}
        for r in rows if r["product_id"] is not None
    ]
    return order
