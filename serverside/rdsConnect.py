import pymysql

host=""
port=3306
dbname="theia_db"
user="admin"
password=""

try:
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
    if conn:
        print('Connected to database')
except Exception as e:
        print("Error Connecting to Database: {}".format(e))


def insertTest():
    insert_statement = "INSERT INTO Account(id,name,username,password) VALUES (2,'John Bro', 'yuser', 'passy');"
    try:
        cursorObject        = conn.cursor()                                     
        sqlQuery            = insert_statement
        cursorObject.execute(sqlQuery)
        cursorObject.execute("SELECT * FROM Account")
        rows = cursorObject.fetchall()
        print(rows)

    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        conn.commit()
        print("Data Successfully Inserted")   
        conn.close()

def queryTest():
    try:
        cursorObject        = conn.cursor()                                     
        cursorObject.execute("SELECT * FROM Account")
        rows = cursorObject.fetchall()
        print(rows)

    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        conn.close()

#queryTest()