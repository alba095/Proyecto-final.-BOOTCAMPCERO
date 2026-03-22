import sqlite3

def init_db():
    conn = sqlite3.connect("movements.db")
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS movimientos
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         fecha TEXT,
         hora TEXT,
         moneda_from TEXT ,
         cantidad_from FLOAT,
         moneda_to TEXT,
         cantidad_to FLOAT
         )
         """)
    conn.commit()
    conn.close()

def get_mov():
    conn = sqlite3.connect("movements.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM movimientos"
    )
    mov = cursor.fetchall()
    conn.close()
    return mov

def add_mov(moneda_from,cantidad_from,moneda_to, cantidad_to):
    conn = sqlite3.connect("movements.db")
    cursor = conn.cursor()
    from datetime import date, datetime
    fecha = date.today().isoformat()
    hora = datetime.now().time().isoformat()
    cursor.execute(
        "INSERT INTO movimientos (fecha, hora,moneda_from,cantidad_from,moneda_to,cantidad_to) VALUES(?,?,?,?,?,?)",
        (fecha,hora,moneda_from,cantidad_from,moneda_to,cantidad_to)
    )
    conn.commit()
    conn.close()

def get_saldo(moneda):
    conn = sqlite3.connect("movements.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to = ?",
        (moneda,)
    )
    
    saldo = cursor.fetchone()[0]
    if saldo == None :
        saldo = 0

    cursor.execute(
        "SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from = ?",
        (moneda,)
    )
    sale = cursor.fetchone()[0]
    if sale == None:
        sale = 0
        
    saldo_final = saldo - sale 
    conn.close() 

    return saldo_final
    
    
