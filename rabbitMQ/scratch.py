#!/bin/python
import mysql
import mysql.connector

def mysql_query_execute(query):
    conn = mysql.connector.connect(user='theia', password='password',
                                   host='localhost',
                                   database='theia')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    result = cur.fetchall()
    return result

def some_task():
    sql = "select id, imageLocation, labels, detect_text, file_date from jsondata"
    results = mysql_query_execute(query=sql)
    for rows in results:
        print(rows)

if __name__ == '__main__':
    some_task()