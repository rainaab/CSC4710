
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "real_estate.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

# Example: Sell SpongeBob's pineapple house
property_address = "124 Conch Street"
buyer_email = "gary@bikinibottom.example"
selling_agent_email = "spongebob@bikinibottom.example"
buyer_agent_email = None

sale_price = 415000
sale_date = "2026-11-05"

try:
    # find the available listing
    cursor.execute("""
        SELECT l.listing_id
        FROM Listing l
        JOIN Property p ON l.property_id = p.property_id
        WHERE p.address = ?
          AND l.status = 'Available';
    """, (property_address,))

    listing = cursor.fetchone()

    if listing is None:
        raise ValueError("No available listing found.")

    listing_id = listing[0]

    # find buyer
    cursor.execute(
        "SELECT buyer_id FROM Buyer WHERE email = ?;",
        (buyer_email,)
    )
    buyer = cursor.fetchone()

    if buyer is None:
        raise ValueError("Buyer not found.")

    # find selling agent
    cursor.execute(
        "SELECT agent_id FROM Agent WHERE email = ?;",
        (selling_agent_email,)
    )
    selling_agent = cursor.fetchone()

    if selling_agent is None:
        raise ValueError("Selling agent not found.")

    # find buyer agent (optional)
    buyer_agent_id = None

    if buyer_agent_email:
        cursor.execute(
            "SELECT agent_id FROM Agent WHERE email = ?;",
            (buyer_agent_email,)
        )
        buyer_agent = cursor.fetchone()

        if buyer_agent is None:
            raise ValueError("Buyer agent not found.")

        buyer_agent_id = buyer_agent[0]

    # start transaction
    conn.execute("BEGIN TRANSACTION;")

    # insert completed sale
    cursor.execute("""
        INSERT INTO Sale (
            listing_id, buyer_id, selling_agent_id,
            buyer_agent_id, sale_price, sale_date
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        listing_id,
        buyer[0],
        selling_agent[0],
        buyer_agent_id,
        sale_price,
        sale_date
    ))

    # update listing status
    cursor.execute("""
        UPDATE Listing
        SET status = 'Sold'
        WHERE listing_id = ?;
    """, (listing_id,))

    conn.commit()
    print("Sale recorded successfully!")
    print(f"Property: {property_address}")
    print(f"Sale Price: ${sale_price:,.2f}")
    print("Listing Status: Sold")

except (sqlite3.Error, ValueError) as error:
    conn.rollback()
    print(f"Transaction failed: {error}")

finally:
    conn.close()
