import pymysql
import pymysql.cursors
import os

def conectar_bd():
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="escola",
        cursorclass=pymysql.cursors.DictCursor
    )
    return con, con.cursor()

def fechar_bd(con, cur):
    cur.close()
    con.close()
