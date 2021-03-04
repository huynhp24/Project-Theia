import pymysql

host="127.0.0.1"
port=3306
dbname="theia"
user="root"
password="root"

conn = pymysql.connect(host=host,user=user,port=port,password=password,database=dbname)

def insertAccount(data):
    print("Inserting Account")
    insert_statement = "INSERT INTO account(name,username,password) VALUES ('{name}','{username}','{password}');".format(**data)
    try:
        cursorObject        = conn.cursor()                                     
        sqlQuery            = insert_statement
        cursorObject.execute(sqlQuery)

    except Exception as e:
        print("Exeception occured:{}".format(e))
        print("Account Not Inserted")
        result = pullAccount(data)
        return result
    else:
        conn.commit()
        print("Account Successfully Inserted")  
        result = pullAccount(data)
        return result 
        conn.close()

def pullAccount(data):

    pull_statement = "SELECT * FROM account WHERE name = '{name}' and username = '{username}' and password = '{password}';".format(**data)
    try:
        cursorObject        = conn.cursor()                                     
        sqlQuery            = pull_statement
        cursorObject.execute(sqlQuery)
        result = cursorObject.fetchall()
        return result

    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        conn.commit()
        print("Account Found:")   
        conn.close()


data = {'name': 'Huynh', 'username': 'quad', 'password': 'hashbrown'}
output = insertAccount(data)
print(output)