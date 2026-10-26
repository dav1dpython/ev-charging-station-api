def charge_battery(battery: int):
    if battery > 100 or battery < 0:
        raise ValueError("Неверный начальный заряд!")
    battery += 20 
    if battery > 100:
        battery = 100
    return battery 

def discharge_battery(battery: int):
    battery -= 10
    if battery < 0:
        battery = 0
    return battery 
         
cars = [40, 70, 95]
charged_cars = []
for battery in cars:
    new_charge = charge_battery(battery)
    charged_cars.append(new_charge)
print(charged_cars)
print(new_charge)

car = {"brand": "Nissan Leaf", "battery": 70}
new_car = charge_battery(car["battery"])
car["battery"] = new_car

fleet = [
    {"brand": "Tesla", "battery": 40},
    {"brand": "Nissan Leaf", "battery": 70},
    {"brand": "Audi e-tron", "battery": 95}
]
for car in fleet:
    new_car = charge_battery(car["battery"])
    car["battery"] = new_car
#print(fleet)
print(f'Машина {car["brand"]}, заряжена на {car["battery"]}%')    

bad_battery = "сорок"
try:
    charge_battery(bad_battery)
except TypeError:
    print("Ошибка! Неверный тип данных")
wrong_battery = 500
try:
    charge_battery(wrong_battery)
except ValueError:
    print("Ошибка! Заряд должен быть от 0 до 100!") 
     