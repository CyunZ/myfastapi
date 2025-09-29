import pyodbc

def selectSQL(sql):
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=127.0.0.1;'
        'DATABASE=MyTEST;'
        'UID=sa;'
        'PWD=123456'
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cols = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()
    return rows,cols