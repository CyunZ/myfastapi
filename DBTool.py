import pyodbc

def selectSQL(sql,params=()):
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=127.0.0.1;'
        'DATABASE=MyTEST;'
        'UID=sa;'
        'PWD=123456'
    )
    cursor = conn.cursor()
    cursor.execute(sql,params)
    rows = cursor.fetchall()
    cols = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()
    return rows,cols


def insertSQL(sql,params=()):
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=127.0.0.1;'
        'DATABASE=MyTEST;'
        'UID=sa;'
        'PWD=123456'
    )
    cursor = conn.cursor()
    try:
        cursor.execute(sql,params)
        cursor.commit()
    except pyodbc.Error as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()