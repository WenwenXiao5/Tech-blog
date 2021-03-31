import psycopg2

connection = psycopg2.connect('postgres://nicoco:@localhost:5432/techblog')

cursor =  connection.cursor()

cursor.execute('select * from tests')
records =  cursor.fetchall()

for record in records:
    print(record)

