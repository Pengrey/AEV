import sqlite3

def initDB():
    # Connecting to sqlite
    # connection object
    connection_obj = sqlite3.connect('/challenge/app/data/creds.db')
    
    # cursor object
    cursor_obj = connection_obj.cursor()
    
    connection_obj.execute("""CREATE TABLE USERS(
    email varchar(50) PRIMARY KEY,
    password varchar(50) COLLATE BINARY
    );""")
    
    connection_obj.execute("""INSERT INTO USERS (email,password) VALUES ("admin@ua.pt","superduperhypersecretpassword")""")
    
    connection_obj.commit()
    
    # Close the connection
    connection_obj.close()

if __name__ == "__main__":
    initDB()