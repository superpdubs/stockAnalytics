import sqlite3
conn = sqlite3.connect('myfetch.db')

c = conn.cursor()
c.execute('SELECT * FROM stock')
print(c.fetchall())
conn.close()
