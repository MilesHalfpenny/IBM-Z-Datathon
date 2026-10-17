import sqlite3

usersConn = sqlite3.connect('users.db')
usercursor = usersConn.cursor()
dietaryConn = sqlite3.connect('dietary.db')
dietcursor = dietaryConn.cursor()

users_table = ('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY UNIQUE,
        id INTEGER NOT NULL AUTOINCREMENT
)
''')
dietary_table = (
    '''CREATE TABLE IF NOT EXISTS dietary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        FOREIGN KEY (username) REFERENCES users_table(username),
        dietary BOOLEAN
    )
'''
)
dietaryConn.commit()
dietcursor.close()
dietcursor.close()
usersConn.commit()
usercursor.close()
usercursor.close()

# cursor.execute(users_table)
# usersConn.commit()

# restriction = input("What is your dietary restriction?") # this would be T/F checklist


# try:

#     cursor.execute('''
#     INSERT INTO recipe (dietary) 
#     VALUES (?, ?)
#     ''', (restriction))
#     conn.commit()

#     print("All data was added")

# except sqlite3.IntegrityError as e:
#     print("Integrity Error", e)

# cursor.execute('''
#     SELECT dietary FROM recipes
# ''')



# conn.commit()
# cursor.close()
# conn.close()