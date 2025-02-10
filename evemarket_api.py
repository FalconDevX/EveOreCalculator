import requests

def get_system_id_by_station(station_id: int):
    """ Pobiera system gwiezdny dla danej stacji """
    url = f"https://esi.evetech.net/latest/universe/stations/{station_id}/?datasource=tranquility"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("system_id")
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd pobierania danych stacji {station_id}: {e}")
        return None

def get_constellation_id_by_system(system_id: int):
    """ Pobiera konstelację na podstawie systemu gwiezdnego """
    url = f"https://esi.evetech.net/latest/universe/systems/{system_id}/?datasource=tranquility"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("constellation_id")
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd pobierania danych systemu {system_id}: {e}")
        return None

def get_region_id_by_constellation(constellation_id: int):
    """ Pobiera region na podstawie konstelacji """
    url = f"https://esi.evetech.net/latest/universe/constellations/{constellation_id}/?datasource=tranquility"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("region_id")
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd pobierania danych konstelacji {constellation_id}: {e}")
        return None

def get_region_id_by_station(station_id: int):
    """ Pobiera ID regionu na podstawie ID stacji """
    system_id = get_system_id_by_station(station_id)
    if system_id is None:
        print(f"⚠️ Nie znaleziono systemu dla stacji {station_id}.")
        return None

    constellation_id = get_constellation_id_by_system(system_id)
    if constellation_id is None:
        print(f"⚠️ Nie udało się znaleźć ID konstelacji dla systemu {system_id}.")
        return None

    region_id = get_region_id_by_constellation(constellation_id)
    if region_id is None:
        print(f"⚠️ Nie udało się znaleźć ID regionu dla konstelacji {constellation_id}.")
        return None

    return region_id

def get_station_name_by_id(station_id: int) -> str:
    """ Pobiera nazwę stacji na podstawie ID """
    url = f"https://esi.evetech.net/latest/universe/stations/{station_id}/?datasource=tranquility"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("name", "Unknown Station")  
    except requests.exceptions.RequestException:
        return "Unknown Station"

def get_best_buy_order(item_id: int, min_quantity: int, station_id: int = 60003760):
    """ Pobiera najlepszą ofertę kupna dla danego przedmiotu na wybranej stacji """
    region_id = get_region_id_by_station(station_id)
    if not region_id:
        print(f"⚠️ Nie udało się znaleźć ID regionu dla stacji {station_id}.")
        return None

    url = f"https://esi.evetech.net/latest/markets/{region_id}/orders/?type_id={item_id}&order_type=buy"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        orders = response.json()

        buy_orders = [
            order for order in orders
            if order.get("location_id") == station_id and order.get("volume_remain", 0) >= min_quantity
        ]

        if not buy_orders:
            print(f"⚠️ Brak ofert kupna dla item_id {item_id} na stacji {station_id}.")
            return None

        best_order = max(buy_orders, key=lambda x: x["price"])

        return {
            "price": best_order["price"],
            "quantity": best_order["volume_remain"],
            "station_id": station_id,
            "station_name": get_station_name_by_id(station_id)
        }
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd podczas pobierania danych: {e}")
        return None

def get_best_buy_order_region(item_id: int, min_quantity: int, region_name: str = "The Forge"):
    """ Pobiera najlepszą ofertę kupna dla danego przedmiotu w całym regionie """
    region_id = get_region_id_by_name(region_name)
    if not region_id:
        print(f"⚠️ Nie znaleziono regionu: {region_name}")
        return None

    url = f"https://esi.evetech.net/latest/markets/{region_id}/orders/?type_id={item_id}&order_type=buy"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        orders = response.json()

        buy_orders = [order for order in orders if order.get("volume_remain", 0) >= min_quantity]

        if not buy_orders:
            print(f"⚠️ Brak dostępnych ofert kupna dla item_id {item_id} w regionie {region_name}.")
            return None

        best_order = max(buy_orders, key=lambda x: x["price"])
        station_name = get_station_name_by_id(best_order["location_id"])

        return {
            "price": best_order["price"],
            "quantity": best_order["volume_remain"],
            "station_id": best_order["location_id"],
            "station_name": station_name
        }
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd podczas pobierania danych: {e}")
        return None

def get_region_id_by_name(region_name: str):
    """ Pobiera ID regionu na podstawie nazwy """
    region_map = {
        "The Forge": 10000002,
        "Domain": 10000043,
        "Sinq Laison": 10000032,
        "Heimatar": 10000030,
        "Metropolis": 10000042
    }
    return region_map.get(region_name, None)


