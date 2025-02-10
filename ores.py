import csv
from evemarket_api import get_best_buy_order, get_best_buy_order_region
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from colorama import Fore, Style

ore_data_file = "OreData.csv"
stations_names_file = "StationsNamesID.csv"

ore_data = {}
with open(ore_data_file, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  
    name_index = header.index("Name")  
    volume_index = header.index("volume")  
    id_index = header.index("ID")  

    for row in reader:
        ore_data[row[name_index]] = {
            "volume": float(row[volume_index]), 
            "ID": int(row[id_index])  
        }

def load_stations(file_path):
    stations = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            station_id = row[0]  
            station_name = row[1]  
            stations[station_name] = station_id
    return stations

def get_station_id(station_name, stations):
    return stations.get(station_name, None)

ore_names = list(ore_data.keys())
completer = WordCompleter(ore_names, ignore_case=True)

stations = load_stations(stations_names_file)
station_completer = WordCompleter(stations.keys(), ignore_case=True)

while True:
    ore_name = prompt("Provide ore name: ", completer=completer)
    if ore_name in ore_data:
        ore_base_volume = ore_data[ore_name]["volume"]
        ore_index = ore_data[ore_name]["ID"]
        print(f"\nYou selected: {ore_name} 🪨")
        print(f"📦 Volume per unit: {ore_base_volume} m³")
        print(f"🔢 Ore ID: {ore_index}")
        break
    else:
        print("❌ Invalid ore name! Please choose from the list.")

while True:
    ore_counter_type = input("Provide ore counter type (v/V - volume, u/U - unit): ")
    if ore_counter_type.lower() == "v":
        while True:
            try:
                ore_volume = float(input("Provide ore volume: "))
                ore_unit = int(ore_volume / ore_base_volume)
                print(f"\nYou provided: {ore_volume} m³ (id: {ore_index}) and it is equal to {ore_unit} units of {ore_name} 🪨")
                break
            except ValueError:
                print("❌ Invalid volume! Please provide a number.")
        break
    elif ore_counter_type.lower() == "u":
        while True:
            try:
                ore_unit = int(input("Provide ore unit: "))
                ore_volume = ore_unit * ore_base_volume
                print(f"\nYou provided: {ore_unit} units and it is equal to {ore_volume} m³ of {ore_name} 🪨")
                break
            except ValueError:
                print("❌ Invalid unit! Please provide a number.")
        break

while True:
    try:
        user_station = prompt("Provide station: ", completer=station_completer)
        station_id = get_station_id(user_station, stations)
        if station_id is None:
            print("❌ Invalid station! Please provide a correct station name.")
        else:
            print(f"ID stacji '{user_station}': {station_id}")
            station_id = int(station_id)
            break
    except ValueError:
        print("❌ Invalid station! Please provide a correct station name.")

print("---------------------------------------------------------------------------------------------------")

best_order_station = get_best_buy_order(ore_index, ore_unit, station_id)
if best_order_station:
    total_income_station = ore_unit * best_order_station["price"]
    print(f"Price per unit ore in station: {Fore.CYAN}{best_order_station['price']}{Style.RESET_ALL}")
    print(f"Quantity unit ore in station: {Fore.YELLOW}{best_order_station['quantity']}{Style.RESET_ALL}")
    print(f"Your total est. income in station: {Fore.GREEN}{total_income_station:,.0f} ISK{Style.RESET_ALL}")
else:
    print(Fore.RED + "Brak dostępnych ofert kupna na tej stacji." + Style.RESET_ALL)

print("---------------------------------------------------------------------------------------------------")

best_order_jita = get_best_buy_order(ore_index, ore_unit, 60003760)
if best_order_jita:
    jita_price_per_unit_ore = best_order_jita["price"]
    jita_quantity_unit_ore = best_order_jita["quantity"]
    total_income_jita = ore_unit * jita_price_per_unit_ore
    print(f"Price per unit ore in Jita 4-4: {Fore.CYAN}{jita_price_per_unit_ore}{Style.RESET_ALL}")
    print(f"Quantity unit ore in Jita 4-4: {Fore.YELLOW}{jita_quantity_unit_ore}{Style.RESET_ALL}")
    print(f"Your total est. income in Jita 4-4: {Fore.GREEN}{total_income_jita:,.0f} ISK{Style.RESET_ALL}")
else:
    print(Fore.RED + "Brak dostępnych ofert kupna w Jita 4-4." + Style.RESET_ALL)

print("---------------------------------------------------------------------------------------------------")

best_order_region_forge = get_best_buy_order_region(ore_index, ore_unit, "The Forge")
if best_order_region_forge:
    print(f"Najlepsza oferta w regionie The Forge: {best_order_region_forge}")
else:
    print(Fore.RED + "Brak dostępnych ofert kupna w regionie The Forge." + Style.RESET_ALL)
