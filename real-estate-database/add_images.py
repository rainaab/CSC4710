import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "real_estate.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

# Property addresses and their corresponding image paths
property_images = [
    ("images/sponge.jpg", "124 Conch Street"),
    ("images/squid.jpg", "122 Conch Street"),
    ("images/pat.jpg", "120 Conch Street"),
    ("images/sandy.jpg", "1 Treedome Drive"),
    ("images/krabs.jpg", "10 Anchor Way"),
    ("images/neptune.webp", "1 Neptune Palace"),
    ("images/pickle.jpeg", "22 Kelp Avenue"),
    ("images/cup.png", "13 Seaweed Street"),

]

cursor.executemany("""
UPDATE Property
SET image_url = ?
WHERE address = ?;
""", property_images)

conn.commit()
print("Property images updated successfully!")


print("\nVERIFYING PROPERTY IMAGES")
print("=" * 55)

cursor.execute("""
SELECT address, image_url
FROM Property
WHERE image_url IS NOT NULL;
""")

properties = cursor.fetchall()

valid_images = 0

for address, image_path in properties:
    full_path = DB_PATH.parent / image_path

    if full_path.is_file():
        print(f"PASS: {address} -> {image_path}")
        valid_images += 1
    else:
        print(f"MISSING FILE: {address} -> {image_path}")

print("\n" + "=" * 55)
print(f"Properties with image paths: {len(properties)}")
print(f"Valid image files: {valid_images}")


conn.close()
