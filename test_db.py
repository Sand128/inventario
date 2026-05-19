from app.database import engine

try:
    conn = engine.connect()
    print("Conexión exitosa")
    conn.close()
except Exception as e:
    print(e)