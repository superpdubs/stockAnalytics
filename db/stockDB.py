import sqlite3, csv
conn = sqlite3.connect('myfetch.db')
c = conn.cursor()
c.execute('''drop table if exists stock''')

c.execute('''
          CREATE TABLE if not exists stock
          (id integer primary key autoincrement,Symbol varchar(10) NOT NULL,Name varchar(50) NOT NULL)
          ''')
with open('nasdaqcompanylist.csv','r') as fin:
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Symbol'], i['Name']) for i in dr]
c.executemany("INSERT INTO stock (Symbol, Name) VALUES (?, ?);", to_db)

with open('nysecompanylist.csv','r') as fin:
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Symbol'], i['Name']) for i in dr]
c.executemany("INSERT INTO stock (Symbol, Name) VALUES (?, ?);", to_db)

conn.commit()
conn.close()
