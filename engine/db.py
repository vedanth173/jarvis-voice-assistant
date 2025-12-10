import csv
import sqlite3

con= sqlite3.connect("jarvis.db")
cursor = con.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)

# Clean up existing WhatsApp entries
##cursor.execute("DELETE FROM sys_command WHERE name LIKE '%whatsapp%'")
##cursor.execute("DELETE FROM web_command WHERE name LIKE '%whatsapp%'")
##con.commit()

# Add WhatsApp Desktop and Web entries
#cursor.execute("INSERT INTO sys_command VALUES (null, 'whatsapp', 'C:\Users\sudee\AppData\Local\WhatsApp\WhatsApp.exe')")
cursor.execute("INSERT INTO web_command VALUES (null, 'Spotify', 'https://open.spotify.com/?flow_ctx=234b0fa1-95b3-401e-a957-61437d716bd7%3A1762260403')")
con.commit()
con.commit()

### testing module
##app_name = "android studio"
##cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
##results = cursor.fetchall()
##print(results[0][0])

##cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL, address VARCHAR(255) NULL)''')

##desired_columns_indices = [0, 30]

# # Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
 #    csvreader = csv.reader(csvfile)
  #   for row in csvreader:
   #      selected_data = [row[i] for i in desired_columns_indices]
    #     cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
#con.commit()
#con.close()

#query = 'Srujan Kondli'
#query = query.strip().lower()
#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#print(results[0][0])


#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')






# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
#desired_columns_indices = [0, 18]

# Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
 #   csvreader = csv.reader(csvfile)
#    for row in csvreader:
#        selected_data = [row[i] for i in desired_columns_indices]
   #     cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
#con.commit()
#con.close()

