import sqlite3

# connect to database
conn = sqlite3.connect("real_estate.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

print("Successfully connected to Real Estate Database!")

# ---------------------------------------------------------------------
# table creations

# create Agent table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Agent (
    agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);
""")

# create Buyer table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Buyer (
    buyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20)
);
""")

# create Seller table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Seller (
    seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20)
);
""")

# save changes
conn.commit()

print("Agent, Buyer, and Seller tables created successfully!")

# create Property table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Property (
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    address VARCHAR(150) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10),
    school_district VARCHAR(100),
    property_type VARCHAR(50),
    bedrooms INTEGER,
    bathrooms DECIMAL(3,1),
    square_feet INTEGER,
    has_pool BOOLEAN DEFAULT FALSE,
    image_url VARCHAR(500)
);
""")

print("Property table created successfully!")


# create Listing table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Listing (
    listing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    listing_agent_id INTEGER NOT NULL,
    list_price DECIMAL(12,2) NOT NULL,
    listing_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Available',

    FOREIGN KEY (property_id) REFERENCES Property(property_id),
    FOREIGN KEY (seller_id) REFERENCES Seller(seller_id),
    FOREIGN KEY (listing_agent_id) REFERENCES Agent(agent_id)
);
""")

print("Listing table created successfully!")

# create Sale table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Sale (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL UNIQUE,
    buyer_id INTEGER NOT NULL,
    selling_agent_id INTEGER NOT NULL,
    buyer_agent_id INTEGER,
    sale_price DECIMAL(12,2) NOT NULL,
    sale_date DATE NOT NULL,

    FOREIGN KEY (listing_id) REFERENCES Listing(listing_id),
    FOREIGN KEY (buyer_id) REFERENCES Buyer(buyer_id),
    FOREIGN KEY (selling_agent_id) REFERENCES Agent(agent_id),
    FOREIGN KEY (buyer_agent_id) REFERENCES Agent(agent_id)
);
""")

print("Sale table created successfully!")


# table checks
cursor.execute("""
SELECT name FROM sqlite_master
WHERE type = 'table'
AND name NOT LIKE 'sqlite_%';
""")
print("\nCurrent tables:")
for table in cursor.fetchall():
    print(table[0])

## KEEP AT END OF CODE. CLOSES CONNECTION
conn.close()