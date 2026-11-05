
import sqlite3
from pathlib import Path
from PIL import Image

DB_PATH = Path(__file__).resolve().parent / "real_estate.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

print("Connected to Bikini Bottom Realty Database!\n")

# ---------------------------------------------------------------------
# query 1: available homes in bikini bottom
# properties priced between $200,000 and $500,000

cursor.execute("""
SELECT
    p.address,
    p.city,
    p.property_type,
    p.bedrooms,
    l.list_price
FROM Property p
JOIN Listing l
    ON p.property_id = l.property_id
WHERE p.city = 'Bikini Bottom'
    AND l.status = 'Available'
    AND l.list_price BETWEEN 200000 AND 500000
ORDER BY l.list_price ASC;
""")

results = cursor.fetchall()

print("QUERY 1: Available Bikini Bottom Homes ($200K-$500K)")
print("-" * 65)

for address, city, property_type, bedrooms, price in results:
    print(
        f"{address} | {city} | {property_type} | "
        f"{bedrooms} beds | ${price:,.2f}"
    )

print(f"\nTotal matching properties: {len(results)}")

# ---------------------------------------------------------------------
# query 2: all homes in Jellyfish Fields with at least 4 bedrooms and no pool

cursor.execute("""
SELECT
    p.address,
    p.city,
    p.bedrooms,
    p.bathrooms,
    p.has_pool,
    l.list_price
FROM Property p
JOIN Listing l
    ON p.property_id = l.property_id
WHERE p.city = 'Jellyfish Fields'
    AND p.bedrooms >= 4
    AND p.has_pool = 0
ORDER BY l.list_price ASC;
""")

results = cursor.fetchall()

print("\nQUERY 2: Jellyfish Fields Homes (4+ Beds, No Pool)")
print("-" * 65)

for address, city, bedrooms, bathrooms, pool, price in results:
    print(
        f"{address} | {bedrooms} beds | "
        f"{bathrooms} baths | No Pool | ${price:,.2f}"
    )

print(f"\nTotal matching properties: {len(results)}")

# ---------------------------------------------------------------------
# query 3: top-selling agent by total sales volume in 2026

cursor.execute("""
SELECT
    a.first_name || ' ' || a.last_name AS agent_name,
    COUNT(s.sale_id) AS total_sales,
    SUM(s.sale_price) AS total_sales_volume
FROM Agent a
JOIN Sale s
    ON a.agent_id = s.selling_agent_id
WHERE s.sale_date BETWEEN '2026-01-01' AND '2026-12-31'
GROUP BY a.agent_id, a.first_name, a.last_name
ORDER BY total_sales_volume DESC
LIMIT 1;
""")

result = cursor.fetchone()

print("\nQUERY 3: Top-Selling Agent in 2026")
print("-" * 65)

if result:
    agent, total_sales, volume = result
    print(f"Agent: {agent}")
    print(f"Properties Sold: {total_sales}")
    print(f"Total Sales Volume: ${volume:,.2f}")
else:
    print("No sales found for 2026.")

# ---------------------------------------------------------------------
# query 4: average sale price and days on market by agent

cursor.execute("""
SELECT
    a.first_name || ' ' || a.last_name AS agent_name,
    COUNT(s.sale_id) AS properties_sold,
    ROUND(AVG(s.sale_price), 2) AS avg_sale_price,
    ROUND(
        AVG(julianday(s.sale_date) - julianday(l.listing_date)),
        1
    ) AS avg_days_on_market
FROM Agent a
JOIN Sale s
    ON a.agent_id = s.selling_agent_id
JOIN Listing l
    ON s.listing_id = l.listing_id
GROUP BY a.agent_id, a.first_name, a.last_name
ORDER BY avg_sale_price DESC;
""")

results = cursor.fetchall()

print("\nQUERY 4: Agent Sales Performance")
print("-" * 75)

for agent, sold, avg_price, avg_days in results:
    print(
        f"{agent} | {sold} sales | "
        f"Avg Price: ${avg_price:,.2f} | "
        f"Avg Days: {avg_days}"
    )
# ---------------------------------------------------------------------
# query 5: Most expensive listed property

print("\nQUERY 5: MOST EXPENSIVE PROPERTY")
print("=" * 60)

cursor.execute("""
SELECT
    p.address,
    p.city,
    p.property_type,
    p.bedrooms,
    p.bathrooms,
    p.square_feet,
    l.list_price,
    l.status,
    p.image_url
FROM Property p
JOIN Listing l ON p.property_id = l.property_id
ORDER BY l.list_price DESC
LIMIT 1;
""")

property_data = cursor.fetchone()

if property_data:
    (
        address, city, property_type,
        bedrooms, bathrooms, square_feet,
        price, status, image_path
    ) = property_data

    print(f"Address: {address}")
    print(f"City: {city}")
    print(f"Property Type: {property_type}")
    print(f"Bedrooms: {bedrooms}")
    print(f"Bathrooms: {bathrooms}")
    print(f"Square Feet: {square_feet:,}")
    print(f"Listing Price: ${price:,.2f}")
    print(f"Status: {status}")

    if image_path:
        full_path = Path(__file__).resolve().parent / image_path

        if full_path.is_file():
            print(f"Image: {image_path}")
            with Image.open(full_path) as img:
                img.show()
        else:
            print(f"Image file not found: {full_path}")
    else:
        print("Image: Not available")
else:
    print("No properties found.")

# ---------------------------------------------------------------------
# query 6 verification: Confirm the completed sale (actual query in "record-sale.py")

cursor.execute("""
SELECT
    p.address,
    b.first_name || ' ' || b.last_name AS buyer,
    s.sale_price,
    s.sale_date,
    l.status
FROM Sale s
JOIN Listing l ON s.listing_id = l.listing_id
JOIN Property p ON l.property_id = p.property_id
JOIN Buyer b ON s.buyer_id = b.buyer_id
WHERE p.address = '124 Conch Street';
""")

result = cursor.fetchone()

print("\nQUERY 6: Verify Completed Sale")
print("-" * 65)

if result:
    address, buyer, price, date, status = result
    print(f"Property: {address}")
    print(f"Buyer: {buyer}")
    print(f"Sale Price: ${price:,.2f}")
    print(f"Sale Date: {date}")
    print(f"Listing Status: {status}")
else:
    print("Sale record not found.")

# ---------------------------------------------------------------------
# query 7: verify new agent (actual query in "add_agent.py")

cursor.execute("""
SELECT agent_id, first_name, last_name, email
FROM Agent
WHERE email = 'puff.agent@bikinibottom.example';
""")

result = cursor.fetchone()

print("\nQUERY 7: Verify New Agent")
print("-" * 65)

if result:
    agent_id, first, last, email = result
    print(f"Agent ID: {agent_id}")
    print(f"Name: {first} {last}")
    print(f"Email: {email}")
else:
    print("Agent not found.")


# ---------------------------------------------------------------------
# additional query #1: properties listed above neighborhood average
print("\nQUERY 8: PROPERTIES ABOVE NEIGHBORHOOD AVERAGE")
print("=" * 75)

cursor.execute("""
SELECT
    p.address,
    p.city,
    l.list_price,
    ROUND((
        SELECT AVG(l2.list_price)
        FROM Property p2
        JOIN Listing l2
            ON p2.property_id = l2.property_id
        WHERE p2.city = p.city
    ), 2) AS neighborhood_avg
FROM Property p
JOIN Listing l
    ON p.property_id = l.property_id
WHERE l.list_price > (
    SELECT AVG(l3.list_price)
    FROM Property p3
    JOIN Listing l3
        ON p3.property_id = l3.property_id
    WHERE p3.city = p.city
)
ORDER BY p.city, l.list_price DESC;
""")

results = cursor.fetchall()

for address, city, price, avg_price in results:
    difference = price - avg_price

    print(
        f"{address} | {city} | "
        f"Price: ${price:,.2f} | "
        f"City Avg: ${avg_price:,.2f} | "
        f"Above Avg: ${difference:,.2f}"
    )

print(f"\nTotal properties above average: {len(results)}")

# ---------------------------------------------------------------------
# additional query #2: properties sold at discounts (sold for less than original listing price)
print("\nQUERY 9: BEST REAL ESTATE DEALS")
print("=" * 85)

cursor.execute("""
SELECT
    p.address,
    b.first_name || ' ' || b.last_name AS buyer,
    l.list_price,
    s.sale_price,
    ROUND(l.list_price - s.sale_price, 2) AS savings,
    ROUND(
        (l.list_price - s.sale_price) * 100.0
        / l.list_price, 2
    ) AS discount_percentage
FROM Sale s
JOIN Listing l ON s.listing_id = l.listing_id
JOIN Property p ON l.property_id = p.property_id
JOIN Buyer b ON s.buyer_id = b.buyer_id
WHERE l.list_price > 0
ORDER BY savings DESC;
""")

results = cursor.fetchall()

for address, buyer, list_price, sale_price, savings, discount in results:
    print(
        f"{address} | Buyer: {buyer} | "
        f"Listed: ${list_price:,.2f} | "
        f"Sold: ${sale_price:,.2f} | "
        f"Savings: ${savings:,.2f} ({discount:.2f}%)"
    )

print(f"\nTotal completed sales analyzed: {len(results)}")

# ---------------------------------------------------------------------
# additional query #3: finding homes the meet select buyer request
print("\nQUERY 10: FIND YOUR DREAM HOME")
print("=" * 75)

# Buyer preferences
# (change these to test different searches)
max_budget = 600000
min_bedrooms = 2
preferred_city = "Bikini Bottom"
pool_required = False

cursor.execute("""
SELECT
    p.address,
    p.city,
    p.property_type,
    p.bedrooms,
    p.bathrooms,
    p.has_pool,
    l.list_price,
    p.image_url
FROM Property p
JOIN Listing l ON p.property_id = l.property_id
WHERE l.status = 'Available'
    AND p.property_type != 'Commercial'
    AND l.list_price <= ?
    AND p.bedrooms >= ?
    AND (? IS NULL OR p.city = ?)
    AND (? = 0 OR p.has_pool = 1)
ORDER BY l.list_price ASC;
""", (
    max_budget,
    min_bedrooms,
    preferred_city,
    preferred_city,
    int(pool_required)
))

results = cursor.fetchall()

print(f"Maximum Budget: ${max_budget:,.2f}")
print(f"Minimum Bedrooms: {min_bedrooms}")
print(f"Preferred City: {preferred_city or 'Any'}")
print(f"Pool Required: {'Yes' if pool_required else 'No'}")
print("-" * 75)

if results:
    for (
        address, city, property_type,
        bedrooms, bathrooms, has_pool,
        price, image_path
    ) in results:
        print(
            f"{address} | {city} | {property_type} | "
            f"{bedrooms} Beds | {bathrooms} Baths | "
            f"Pool: {'Yes' if has_pool else 'No'} | "
            f"${price:,.2f}"
        )
else:
    print("No properties match these preferences.")

print(f"\nMatching properties: {len(results)}")

conn.close()
