import requests

def get_system_id_by_station(station_id: int):
    """ Pobiera system gwiezdny dla danej stacji """
    url = f"https://esi.evetech.net/latest/universe/stations/{station_id}/?datasource=tranquility"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        system_id = data.get("system_id")
        if system_id:
            return system_id
        else:
            print(f"⚠️ API nie zwróciło ID systemu dla stacji {station_id}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd pobierania danych stacji {station_id}: {e}")
        return None

def get_region_id_by_system(system_id: int):
    """ Pobiera region na podstawie systemu gwiezdnego """
    if system_id is None:
        print("⚠️ System ID jest None, nie można pobrać regionu.")
        return None

    url = f"https://esi.evetech.net/latest/universe/systems/{system_id}/?datasource=tranquility"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        print(f"🔍 Odpowiedź API dla systemu {system_id}: {data}")  # DEBUG

        region_id = data.get("region_id")
        if region_id:
            return region_id
        else:
            print(f"⚠️ API nie zwróciło ID regionu dla systemu {system_id}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd pobierania danych systemu {system_id}: {e}")
        return None


def get_region_id_by_station(station_id: int):
    """ Pobiera ID regionu na podstawie ID stacji """
    system_id = get_system_id_by_station(station_id)
    if system_id is None:
        print(f"⚠️ Nie znaleziono systemu dla stacji ID {station_id}.")
        return None

    region_id = get_region_id_by_system(system_id)
    if region_id is None:
        print(f"⚠️ Nie udało się znaleźć ID regionu dla systemu {system_id}.")
        return None

    return region_id

# 🔹 **Testowanie funkcji**
if __name__ == "__main__":
    station_id = 60003760  # Jita 4-4
    region_id = get_region_id_by_station(station_id)
    print(f"📍 ID regionu dla stacji {station_id}: {region_id}")
