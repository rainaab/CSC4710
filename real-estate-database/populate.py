
import sqlite3

# connect to our database
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "real_estate.db"
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

print("Connected to Real Estate Database!")

# check that all six tables exist
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
AND name NOT LIKE 'sqlite_%';
""")

tables = cursor.fetchall()

print(f"Found {len(tables)} tables.")


# populate Agent table
agents = [
    ("SpongeBob", "SquarePants", "spongebob@bikinibottom.example", "555-0101"),
    ("Squidward", "Tentacles", "squidward@bikinibottom.example", "555-0102"),
    ("Eugene", "Krabs", "krabs@bikinibottom.example", "555-0103"),
    ("Sandy", "Cheeks", "sandy@bikinibottom.example", "555-0104"),
    ("Patrick", "Star", "patrick@bikinibottom.example", "555-0105"),
    ("Sheldon", "Plankton", "plankton@bikinibottom.example", "555-0106"),
    ("Pearl", "Krabs", "pearl@bikinibottom.example", "555-0107"),
    ("Larry", "Lobster", "larry@bikinibottom.example", "555-0108")
]

#insert or ignore allows us to only take in unique queries
cursor.executemany("""
INSERT OR IGNORE INTO Agent
(first_name, last_name, email, phone)
VALUES (?, ?, ?, ?);
""", agents)

print("Agent data populated successfully!")


# populate Buyer table
buyers = [
    ("Gary", "Snail", "gary@bikinibottom.example", "555-0201"),
    ("Mrs.", "Puff", "puff@bikinibottom.example", "555-0202"),
    ("Karen", "Plankton", "karen@bikinibottom.example", "555-0203"),
    ("Mermaid", "Man", "mermaidman@bikinibottom.example", "555-0204"),
    ("Barnacle", "Boy", "barnacleboy@bikinibottom.example", "555-0205"),
    ("Bubble", "Bass", "bubblebass@bikinibottom.example", "555-0206"),
    ("Fred", "Fish", "fred@bikinibottom.example", "555-0207"),
    ("Tom", "Fish", "tom@bikinibottom.example", "555-0208"),
    ("Harold", "Fish", "harold@bikinibottom.example", "555-0209"),
    ("Nat", "Peterson", "nat@bikinibottom.example", "555-0210"),
    ("Old", "Man Jenkins", "jenkins@bikinibottom.example", "555-0211"),
    ("Flats", "Flounder", "flats@bikinibottom.example", "555-0212"),
    ("Man", "Ray", "manray@bikinibottom.example", "555-0213"),
    ("Dirty", "Bubble", "dirtybubble@bikinibottom.example", "555-0214"),
    ("Patchy", "Pirate", "patchy@bikinibottom.example", "555-0215"),
    ("Potty", "Parrot", "potty@bikinibottom.example", "555-0216"),
    ("Kevin", "Cucumber", "kevin@bikinibottom.example", "555-0217"),
    ("Doodle", "Bob", "doodlebob@bikinibottom.example", "555-0218"),
    ("Flying", "Dutchman", "dutchman@bikinibottom.example", "555-0219"),
    ("King", "Neptune", "neptune@bikinibottom.example", "555-0220")
]

cursor.executemany("""
INSERT OR IGNORE INTO Buyer
(first_name, last_name, email, phone)
VALUES (?, ?, ?, ?);
""", buyers)

print("Buyer data populated successfully!")


# populate Seller table
sellers = [
    ("SpongeBob", "SquarePants", "spongebob.seller@bikinibottom.example", "555-0301"),
    ("Squidward", "Tentacles", "squidward.seller@bikinibottom.example", "555-0302"),
    ("Patrick", "Star", "patrick.seller@bikinibottom.example", "555-0303"),
    ("Sandy", "Cheeks", "sandy.seller@bikinibottom.example", "555-0304"),
    ("Eugene", "Krabs", "krabs.seller@bikinibottom.example", "555-0305"),
    ("Sheldon", "Plankton", "plankton.seller@bikinibottom.example", "555-0306"),
    ("Pearl", "Krabs", "pearl.seller@bikinibottom.example", "555-0307"),
    ("Larry", "Lobster", "larry.seller@bikinibottom.example", "555-0308"),
    ("Mrs.", "Puff", "puff.seller@bikinibottom.example", "555-0309"),
    ("Bubble", "Bass", "bubblebass.seller@bikinibottom.example", "555-0310"),
    ("Fred", "Fish", "fred.seller@bikinibottom.example", "555-0311"),
    ("Tom", "Fish", "tom.seller@bikinibottom.example", "555-0312"),
    ("Harold", "Fish", "harold.seller@bikinibottom.example", "555-0313"),
    ("Nat", "Peterson", "nat.seller@bikinibottom.example", "555-0314"),
    ("Old", "Man Jenkins", "jenkins.seller@bikinibottom.example", "555-0315"),
    ("Flats", "Flounder", "flats.seller@bikinibottom.example", "555-0316"),
    ("Man", "Ray", "manray.seller@bikinibottom.example", "555-0317"),
    ("Karen", "Plankton", "karen.seller@bikinibottom.example", "555-0318"),
    ("Kevin", "Cucumber", "kevin.seller@bikinibottom.example", "555-0319"),
    ("King", "Neptune", "neptune.seller@bikinibottom.example", "555-0320")
]

cursor.executemany("""
INSERT OR IGNORE INTO Seller
(first_name, last_name, email, phone)
VALUES (?, ?, ?, ?);
""", sellers)

conn.commit()
print("Seller data populated successfully!")


# populate Property table
properties = [
    ("124 Conch Street", "Bikini Bottom", "BB", "00001", "Bikini Bottom Central", "Pineapple House", 2, 2.0, 1800, 0, None),
    ("122 Conch Street", "Bikini Bottom", "BB", "00001", "Bikini Bottom Central", "Stone House", 3, 2.0, 2200, 0, None),
    ("120 Conch Street", "Bikini Bottom", "BB", "00001", "Bikini Bottom Central", "Rock House", 1, 1.0, 600, 0, None),
    ("1 Treedome Drive", "Bikini Bottom", "BB", "00002", "Bikini Bottom Science Academy", "Treedome", 4, 3.0, 3500, 0, None),
    ("10 Anchor Way", "Bikini Bottom", "BB", "00003", "Bikini Bottom Central", "Anchor Mansion", 6, 5.0, 7200, 1, None),
    ("5 Chum Bucket Lane", "Bikini Bottom", "BB", "00004", "Bikini Bottom Central", "Commercial", 2, 1.0, 1400, 0, None),
    ("18 Jellyfish Lane", "Jellyfish Fields", "BB", "00005", "Jellyfish Fields Academy", "Coral Cottage", 4, 2.5, 2600, 0, None),
    ("42 Jellyfish Lane", "Jellyfish Fields", "BB", "00005", "Jellyfish Fields Academy", "Coral Cottage", 3, 2.0, 2100, 0, None),
    ("7 Lagoon Boulevard", "Goo Lagoon", "BB", "00006", "Goo Lagoon High", "Beach House", 5, 4.0, 4200, 1, None),
    ("15 Lagoon Boulevard", "Goo Lagoon", "BB", "00006", "Goo Lagoon High", "Beach House", 3, 2.0, 1900, 0, None),
    ("8 Coral Court", "Bikini Bottom", "BB", "00007", "Bikini Bottom Central", "Coral Cottage", 3, 2.0, 1850, 0, None),
    ("16 Coral Court", "Bikini Bottom", "BB", "00007", "Bikini Bottom Central", "Coral Cottage", 4, 3.0, 2750, 1, None),
    ("24 Coral Court", "Bikini Bottom", "BB", "00007", "Bikini Bottom Central", "Townhouse", 2, 1.5, 1350, 0, None),
    ("32 Coral Court", "Bikini Bottom", "BB", "00007", "Bikini Bottom Central", "Townhouse", 3, 2.5, 2050, 0, None),
    ("6 Kelp Avenue", "Bikini Bottom", "BB", "00008", "Kelp Forest Academy", "Condo", 2, 2.0, 1200, 1, None),
    ("14 Kelp Avenue", "Bikini Bottom", "BB", "00008", "Kelp Forest Academy", "Condo", 3, 2.0, 1650, 1, None),
    ("22 Kelp Avenue", "Bikini Bottom", "BB", "00008", "Kelp Forest Academy", "Single Family", 4, 3.0, 2950, 0, None),
    ("30 Kelp Avenue", "Bikini Bottom", "BB", "00008", "Kelp Forest Academy", "Single Family", 5, 4.0, 4100, 1, None),
    ("3 Rock Bottom Road", "Rock Bottom", "BB", "00009", "Rock Bottom High", "Cave House", 2, 1.0, 950, 0, None),
    ("11 Rock Bottom Road", "Rock Bottom", "BB", "00009", "Rock Bottom High", "Cave House", 3, 2.0, 1750, 0, None),
    ("19 Rock Bottom Road", "Rock Bottom", "BB", "00009", "Rock Bottom High", "Stone Villa", 4, 3.0, 3100, 1, None),
    ("27 Rock Bottom Road", "Rock Bottom", "BB", "00009", "Rock Bottom High", "Stone Villa", 5, 3.5, 3900, 0, None),
    ("5 Seaweed Street", "New Kelp City", "BB", "00010", "New Kelp City Academy", "Apartment", 1, 1.0, 750, 0, None),
    ("13 Seaweed Street", "New Kelp City", "BB", "00010", "New Kelp City Academy", "Apartment", 2, 2.0, 1150, 0, None),
    ("21 Seaweed Street", "New Kelp City", "BB", "00010", "New Kelp City Academy", "Penthouse", 3, 3.0, 2800, 1, None),
    ("29 Seaweed Street", "New Kelp City", "BB", "00010", "New Kelp City Academy", "Penthouse", 4, 4.0, 4200, 1, None),
    ("4 Shell Boulevard", "Shell City", "BB", "00011", "Shell City High", "Shell Cottage", 2, 1.5, 1400, 0, None),
    ("12 Shell Boulevard", "Shell City", "BB", "00011", "Shell City High", "Shell Cottage", 3, 2.0, 1950, 0, None),
    ("20 Shell Boulevard", "Shell City", "BB", "00011", "Shell City High", "Luxury Villa", 5, 4.5, 5200, 1, None),
    ("28 Shell Boulevard", "Shell City", "BB", "00011", "Shell City High", "Luxury Villa", 6, 5.0, 6800, 1, None),
    ("9 Reef Road", "Jellyfish Fields", "BB", "00012", "Jellyfish Fields Academy", "Reef House", 3, 2.0, 1900, 0, None),
    ("17 Reef Road", "Jellyfish Fields", "BB", "00012", "Jellyfish Fields Academy", "Reef House", 4, 3.0, 2850, 0, None),
    ("25 Reef Road", "Jellyfish Fields", "BB", "00012", "Jellyfish Fields Academy", "Reef House", 4, 3.5, 3300, 1, None),
    ("33 Reef Road", "Jellyfish Fields", "BB", "00012", "Jellyfish Fields Academy", "Reef House", 5, 4.0, 4500, 1, None),
    ("2 Ocean View Drive", "Goo Lagoon", "BB", "00013", "Goo Lagoon High", "Beach Condo", 2, 2.0, 1450, 1, None),
    ("10 Ocean View Drive", "Goo Lagoon", "BB", "00013", "Goo Lagoon High", "Beach Condo", 3, 2.0, 1850, 1, None),
    ("18 Ocean View Drive", "Goo Lagoon", "BB", "00013", "Goo Lagoon High", "Beach House", 4, 3.0, 3200, 1, None),
    ("26 Ocean View Drive", "Goo Lagoon", "BB", "00013", "Goo Lagoon High", "Beach House", 5, 4.0, 4700, 1, None),
    ("1 Neptune Palace", "Atlantis", "BB", "00014", "Atlantis Royal Academy", "Royal Palace", 10, 8.0, 15000, 1, None),
    ("7 Trident Terrace", "Atlantis", "BB", "00014", "Atlantis Royal Academy", "Luxury Mansion", 7, 6.0, 9500, 1, None),
]

cursor.executemany("""
INSERT INTO Property (
    address, city, state, zip_code, school_district,
    property_type, bedrooms, bathrooms, square_feet,
    has_pool, image_url
)
SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
WHERE NOT EXISTS (
    SELECT 1 FROM Property WHERE address = ? AND city = ?
);
""", [p + (p[0], p[1]) for p in properties])

conn.commit()
print("Property data populated successfully!")

cursor.execute("SELECT COUNT(*) FROM Property;")
print("Total properties:", cursor.fetchone()[0])


# populate Listing table
# format: (property number, seller number, agent number, listing price, listing date, status)

listings = [
    (1, 1, 2, 425000, "2026-01-10", "Available"),
    (2, 2, 3, 510000, "2026-02-05", "Available"),
    (3, 3, 1, 185000, "2026-01-20", "Sold"),
    (4, 4, 5, 875000, "2026-03-01", "Available"),
    (5, 5, 4, 2250000, "2026-02-15", "Sold"),
    (6, 6, 7, 295000, "2026-03-10", "Available"),
    (7, 7, 1, 465000, "2026-01-15", "Sold"),
    (8, 8, 2, 385000, "2026-04-01", "Available"),
    (9, 9, 6, 1100000, "2026-02-20", "Sold"),
    (10, 10, 3, 395000, "2026-04-12", "Available"),
    (11, 11, 4, 365000, "2026-03-05", "Sold"),
    (12, 12, 5, 575000, "2026-04-15", "Available"),
    (13, 13, 6, 275000, "2026-03-20", "Available"),
    (14, 14, 7, 435000, "2026-02-10", "Sold"),
    (15, 15, 8, 325000, "2026-05-01", "Available"),
    (16, 16, 1, 385000, "2026-02-25", "Sold"),
    (17, 17, 2, 625000, "2026-05-12", "Available"),
    (18, 18, 3, 950000, "2026-03-15", "Sold"),
    (19, 19, 4, 215000, "2026-04-05", "Available"),
    (20, 20, 5, 345000, "2026-03-01", "Sold"),
    (21, 1, 6, 685000, "2026-05-20", "Available"),
    (22, 2, 7, 825000, "2026-04-10", "Sold"),
    (23, 3, 8, 195000, "2026-06-01", "Available"),
    (24, 4, 1, 285000, "2026-04-20", "Sold"),
    (25, 5, 2, 725000, "2026-06-10", "Available"),
    (26, 6, 3, 1150000, "2026-05-05", "Sold"),
    (27, 7, 4, 315000, "2026-06-15", "Available"),
    (28, 8, 5, 425000, "2026-06-20", "Available"),
    (29, 9, 6, 1350000, "2026-05-15", "Sold"),
    (30, 10, 7, 1850000, "2026-07-01", "Available"),
    (31, 11, 8, 375000, "2026-07-05", "Available"),
    (32, 12, 1, 495000, "2026-05-25", "Sold"),
    (33, 13, 2, 635000, "2026-07-10", "Available"),
    (34, 14, 3, 895000, "2026-07-15", "Available"),
    (35, 15, 4, 335000, "2026-08-01", "Available"),
    (36, 16, 5, 415000, "2026-08-05", "Available"),
    (37, 17, 6, 765000, "2026-06-05", "Sold"),
    (38, 18, 7, 1250000, "2026-08-10", "Available"),
    (39, 19, 8, 8500000, "2026-09-01", "Available"),
    (40, 20, 1, 4200000, "2026-09-10", "Available")
]

# match each property, seller, and agent by their actual IDs instead of assuming IDs always start at 1.

cursor.execute("SELECT property_id FROM Property ORDER BY property_id;")
property_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT seller_id FROM Seller ORDER BY seller_id;")
seller_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT agent_id FROM Agent ORDER BY agent_id;")
agent_ids = [row[0] for row in cursor.fetchall()]

assert len(property_ids) == 40, "Expected 40 properties."
assert len(seller_ids) == 20, "Expected 20 sellers."
assert len(agent_ids) == 8, "Expected 8 agents."

for property_num, seller_num, agent_num, price, date, status in listings:
    property_id = property_ids[property_num - 1]
    seller_id = seller_ids[seller_num - 1]
    agent_id = agent_ids[agent_num - 1]

    cursor.execute("""
        INSERT INTO Listing (
            property_id, seller_id, listing_agent_id,
            list_price, listing_date, status
        )
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM Listing WHERE property_id = ?
        );
    """, (
        property_id, seller_id, agent_id,
        price, date, status, property_id
    ))

conn.commit()
print("Listing data populated successfully!")

# populate Sale table
# format: (property number, buyer number, selling agent number, buyer agent number, sale price, sale date)

sales = [
    (3, 1, 1, 2, 180000, "2026-02-15"),
    (5, 2, 4, 3, 2180000, "2026-03-20"),
    (7, 3, 1, None, 455000, "2026-02-28"),
    (9, 4, 6, 5, 1075000, "2026-04-10"),
    (11, 5, 4, 1, 360000, "2026-04-18"),
    (14, 6, 7, None, 425000, "2026-03-25"),
    (16, 7, 1, 8, 380000, "2026-04-05"),
    (18, 8, 3, 2, 925000, "2026-05-12"),
    (20, 9, 5, 4, 340000, "2026-04-22"),
    (22, 10, 7, 6, 810000, "2026-05-30"),
    (24, 11, 1, None, 280000, "2026-05-25"),
    (26, 12, 3, 5, 1125000, "2026-06-18"),
    (29, 13, 6, 7, 1325000, "2026-07-02"),
    (32, 14, 1, 3, 485000, "2026-07-15"),
    (37, 15, 6, 8, 750000, "2026-08-20")
]

# retrieve IDs for buyers and agents
cursor.execute("SELECT buyer_id FROM Buyer ORDER BY buyer_id;")
buyer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT agent_id FROM Agent ORDER BY agent_id;")
agent_ids = [row[0] for row in cursor.fetchall()]

assert len(buyer_ids) >= 20, "Expected at least 20 buyers."
assert len(agent_ids) >= 8, "Expected at least 8 agents."

for property_num, buyer_num, selling_num, buyer_agent_num, price, date in sales:
    property_id = property_ids[property_num - 1]
    buyer_id = buyer_ids[buyer_num - 1]
    selling_agent_id = agent_ids[selling_num - 1]

    buyer_agent_id = (
        agent_ids[buyer_agent_num - 1]
        if buyer_agent_num is not None
        else None
    )

    # find the listing associated with property
    cursor.execute("""
        SELECT listing_id
        FROM Listing
        WHERE property_id = ? AND status = 'Sold';
    """, (property_id,))

    result = cursor.fetchone()

    if result is None:
        raise ValueError(f"No sold listing found for property {property_num}")

    listing_id = result[0]

    # avoid duplicates
    cursor.execute("""
        INSERT OR IGNORE INTO Sale (
            listing_id, buyer_id, selling_agent_id,
            buyer_agent_id, sale_price, sale_date
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        listing_id, buyer_id, selling_agent_id,
        buyer_agent_id, price, date
    ))

conn.commit()
print("Sale data populated successfully!")


print("\nFinal Database Summary:")

for table in ["Agent", "Buyer", "Seller", "Property", "Listing", "Sale"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table};")
    print(f"{table}: {cursor.fetchone()[0]} records")


# KEEP AT END OF CODE! CLOSES DB CONNECTION!
conn.close()