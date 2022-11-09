import sqlite3
import requests

# Database connection
conn = sqlite3.connect('/home/fagan/hackedNews/users.db')
c = conn.cursor()

c.execute("INSERT INTO Likes VALUES('32532523', '2432432', 'author', 'title', 'link', True)")

conn.commit()
conn.close()
