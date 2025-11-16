import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "", 
    "database": "escola"
}

def conectar_bd():
    try:
        con = mysql.connector.connect(**DB_CONFIG)
        cur = con.cursor(dictionary=True)
        return con, cur
    except mysql.connector.Error as e:
        print("Erro ao conectar ao banco:", e)
        return None, None

def fechar_bd(con, cur):
    try:
        if cur: cur.close()
        if con: con.close()
    except:
        pass
