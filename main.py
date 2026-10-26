from fastapi import FastAPI, HTTPException
from helpers import charge_battery
import sqlite3
app = FastAPI()

connection = sqlite3.connect("station.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Автоматический уникальный номер машины
    brand TEXT,                            -- Текстовая колонка для марки
    battery INTEGER                        -- Числовая колонка для заряда
)
""")

connection.commit()

@app.get("/status")
def get_station_status():
    return {"status": "all_stations_free", "online": True}

@app.get("/cars/{car_id}")
def get_single_car(car_id: int):
    local_cursor = connection.cursor()
    local_cursor.execute("SELECT brand, battery FROM cars WHERE id = ?", (car_id,))
    
    row = local_cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Car not found in SQL database")
    return {"brand": row[0], "battery": row[1]}

@app.post("/cars")
def add_new_car(brand: str, battery: int):
    local_cursor = connection.cursor()
    
    local_cursor.execute(
        "INSERT INTO cars (brand, battery) VALUES (?, ?)", 
        (brand, battery)
    )
    connection.commit()

    return {"message": f"Машина {brand} НАВСЕГДА добавлена в базу данных SQL!"}

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    local_cursor = connection.cursor()

    local_cursor.execute(
        "DELETE FROM cars WHERE id = ?", (car_id,)
    )
    connection.commit()

    return {"message": f'машина успешно удалена'}

@app.get("/cars")
def get_all_cars():
    local_cursor = connection.cursor()

    local_cursor.execute("SELECT id, brand, battery FROM cars")
    rows = local_cursor.fetchall()

    result = []
    for row in rows:
        car_dict = {"id": row[0], "brand": row[1], "battery": row[2]}
        result.append(car_dict)
    return result 

@app.put("/cars/{car_id}")
def charge_car_by_id(car_id: int):
    local_cursor = connection.cursor()

    local_cursor.execute("SELECT battery FROM cars WHERE id = ?", (car_id,))
    row = local_cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Car not found") 
    
    new_battery = charge_battery(row[0]) 
    local_cursor.execute("UPDATE cars SET battery = ? WHERE id = ?", (new_battery, car_id))
    connection.commit()

    return {"message": f"Машина успешно заряжена! Новый заряд: {new_battery}%"}

