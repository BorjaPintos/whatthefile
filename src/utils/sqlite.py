import sqlite3


def execute_query(path, query: str):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows