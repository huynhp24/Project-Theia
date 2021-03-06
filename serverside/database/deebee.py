import pymysql

host="127.0.0.1"
port=3306
dbname="theia"
user="root"
password="root"

conn = pymysql.connect(host=host,user=user,port=port,password=password,database=dbname)

def insertAccount(data):
    print("1/2-Inserting Account")
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

def insertPicture(data):
    print("1/2-Inserting Picture")
    insert_statement = "INSERT INTO picture(idpicture,name,s3id) VALUES ('{idpicture}','{name}','{s3id}');".format(**data)
    try:
        cursorObject        = conn.cursor()                                     
        sqlQuery            = insert_statement
        cursorObject.execute(sqlQuery)

    except Exception as e:
        print("Exeception occured:{}".format(e))
        print("Picture Not Inserted")
        result = pullPicture(data)
        return result
    else:
        conn.commit()
        print("Picture Successfully Inserted")  
        result = insertAccountPicture(data)
        return result 
        conn.close()

def insertAccountPicture(data):
    print("2/2-Inserting AccountPicture")
    insert_statement = "INSERT INTO acc_pic(user,idpicture) VALUES ('{username}','{idpicture}');".format(**data)
    try:
        cursorObject        = conn.cursor()                                     
        sqlQuery            = insert_statement
        cursorObject.execute(sqlQuery)

    except Exception as e:
        print("Exeception occured:{}".format(e))
        print("PictureAccount Not Inserted")
        result = pullPicture(data)
        return result
    else:
        conn.commit()
        print("PictureAccount Successfully Inserted")  
        result = pullPicture(data)
        return result 
        conn.close()

def pullPicture(data):

    pull_statement = "SELECT account.name, picture.idpicture, picture.name, picture.s3id FROM picture INNER JOIN acc_pic ON picture.idpicture = acc_pic.idpicture INNER JOIN account ON account.username = acc_pic.user WHERE picture.name = '{name}' and acc_pic.user = '{username}' and acc_pic.idpicture = '{idpicture}';".format(**data)
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
        print("Picture Found:")   
        conn.close()

def pullPicturesWithAccount(data):
    
    pull_statement = "SELECT account.name, picture.idpicture, picture.name, picture.s3id FROM picture INNER JOIN acc_pic ON picture.idpicture = acc_pic.idpicture INNER JOIN account ON account.username = acc_pic.user WHERE acc_pic.user = '{username}';".format(**data)
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
        print("Picture Found:")   
        conn.close()

def insertAnalysis(data):
    print("Inserting Analysis")
    insert_statement = "INSERT INTO analysis(idpicture,analysis) VALUES ('{idpicture}','{analysis}');".format(**data)
    try:
        cursorObject        = conn.cursor()                                     
        sqlQuery            = insert_statement
        cursorObject.execute(sqlQuery)

    except Exception as e:
        print("Exeception occured:{}".format(e))
        print("Analysis Not Inserted")
        result = pullAnalysis(data)
        return result
    else:
        conn.commit()
        print("Analysis Successfully Inserted")  
        result = pullAnalysis(data)
        return result 
        conn.close()

def pullAnalysis(data):

    pull_statement = "SELECT picture.name, account.name, analysis.analysis FROM picture INNER JOIN acc_pic ON picture.idpicture = acc_pic.idpicture INNER JOIN account ON account.username = acc_pic.user INNER JOIN analysis ON picture.idpicture = analysis.idpicture WHERE acc_pic.user = '{username}' and analysis.idpicture = '{idpicture}';".format(**data)
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
        print("Analysis Found:")   
        conn.close()

#insert account# data = {'name': 'Huynh', 'username': 'quad', 'password': 'hashbrown'}
#insert picture# data = {'username': 'quad', 'idpicture': '2', 'name': 'pic', 's3id': 's3://d111safdsfafdsa'}
data = {'username': 'quad', 'idpicture': '2', 'analysis': 'Wow dude this is an analysis and it is fantastic'}
output = pullAnalysis(data)
print(output)