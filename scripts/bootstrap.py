#! /usr/env/python3

import sqlite3

item_list = [
    ("Nike", 2000, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8c2hvZXxlbnwwfHwwfHw%3D&w=1000&q=80"),
    ("Adidas", 500, "https://media.istockphoto.com/photos/sport-shoes-on-isolated-white-background-picture-id956501428?k=20&m=956501428&s=612x612&w=0&h=UC4qdZa2iA0PJvv0RIBlJDyF80wxFyLPq4YWvZa30Sc="),
    ("Chuka", 1500, "https://media.istockphoto.com/photos/brown-leather-shoe-picture-id187310279?k=20&m=187310279&s=612x612&w=0&h=WDavpCxsLbj_PRpoY-3PsS2zvuP0Vk0Ci22sRLO9DzE="),
]

conn = sqlite3.connect("microservices/products_api/products.db")
conn.execute("CREATE TABLE IF NOT EXISTS products(name, price, image)")
conn.executemany("INSERT INTO products values(?, ?, ?)", item_list)
conn.commit()
conn.close()