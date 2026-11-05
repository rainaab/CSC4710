
import sqlite3
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "real_estate.db"

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
SELECT
    p.address,
    p.city,
    p.property_type,
    p.bedrooms,
    p.bathrooms,
    l.list_price,
    l.status,
    p.image_url
FROM Property p
JOIN Listing l ON p.property_id = l.property_id
WHERE p.image_url IS NOT NULL
ORDER BY l.list_price DESC;
""")

properties = cursor.fetchall()
conn.close()

# Main window
root = tk.Tk()
root.title("Bikini Bottom Realty | Property Gallery")
root.geometry("1100x750")

title = tk.Label(
    root,
    text="BIKINI BOTTOM REALTY",
    font=("Arial", 24, "bold")
)
title.pack(pady=(15, 2))

subtitle = tk.Label(
    root,
    text="Explore Our Underwater Properties",
    font=("Arial", 12)
)
subtitle.pack(pady=(0, 15))

# Scrollable area
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(
    root, orient="vertical", command=canvas.yview
)
frame = tk.Frame(canvas)

frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Keep references so images remain visible
image_refs = []

for i, property_data in enumerate(properties):
    (
        address, city, property_type,
        bedrooms, bathrooms, price,
        status, image_path
    ) = property_data

    card = tk.Frame(
        frame,
        bd=1,
        relief="solid",
        padx=15,
        pady=15
    )
    card.grid(
        row=i // 2,
        column=i % 2,
        padx=15,
        pady=15,
        sticky="n"
    )

    full_path = BASE_DIR / image_path

    if full_path.is_file():
        with Image.open(full_path) as source:
            img = source.copy()
        img.thumbnail((440, 240))

        photo = ImageTk.PhotoImage(img)
        image_refs.append(photo)

        image_label = tk.Label(card, image=photo)
        image_label.pack()
    else:
        tk.Label(
            card,
            text="Image unavailable",
            width=40,
            height=10
        ).pack()

    tk.Label(
        card,
        text=address,
        font=("Arial", 16, "bold")
    ).pack(pady=(10, 3))

    tk.Label(
        card,
        text=f"{city} | {property_type}"
    ).pack()

    tk.Label(
        card,
        text=f"{bedrooms} Beds | {bathrooms} Baths"
    ).pack(pady=3)

    tk.Label(
        card,
        text=f"${price:,.2f}",
        font=("Arial", 15, "bold")
    ).pack(pady=5)

    tk.Label(
        card,
        text=f"Status: {status}"
    ).pack()

root.mainloop()
