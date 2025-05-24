import requests

def obtener_coordenadas(ciudad):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}"
    respuesta = requests.get(url)
    datos = respuesta.json()

    if 'results' in datos and datos['results']:
        lat = datos['results'][0]['latitude']
        lon = datos['results'][0]['longitude']
        return lat, lon
    else:
        print(f"No se encontraron coordenadas para {ciudad}")
        return None, None

def obtener_clima(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    respuesta = requests.get(url)
    datos = respuesta.json()
    
    clima = datos["current_weather"]
    temperatura = float(clima["temperature"])
    viento = float(clima["windspeed"])
    codigo_clima = int(clima["weathercode"])

    estado_cielo = interpretar_codigo_clima(codigo_clima)

    return round(temperatura, 2), round(viento, 2), estado_cielo

def interpretar_codigo_clima(codigo):
    # Simplificación del código de clima Open-Meteo
    if codigo == 0:
        return "despejado"
    elif codigo in [1, 2, 3]:
        return "parcialmente nublado"
    elif codigo in [45, 48]:
        return "con niebla"
    elif codigo in [51, 53, 55]:
        return "con llovizna"
    elif codigo in [61, 63, 65]:
        return "con lluvia"
    elif codigo in [71, 73, 75]:
        return "con nieve"
    elif codigo in [95, 96, 99]:
        return "con tormenta"
    else:
        return "condiciones climáticas desconocidas"

def main():
    while True:
        print("\n--- Comparador de Clima ---")
        ciudad_origen = input("Ingresa Ciudad de Origen (o 'q' para salir): ")
        if ciudad_origen.lower() == "q":
            break
        ciudad_destino = input("Ingresa Ciudad de Destino (o 'q' para salir): ")
        if ciudad_destino.lower() == "q":
            break

        lat_origen, lon_origen = obtener_coordenadas(ciudad_origen)
        lat_destino, lon_destino = obtener_coordenadas(ciudad_destino)

        if None in [lat_origen, lon_origen, lat_destino, lon_destino]:
            print("No se pudieron obtener las coordenadas correctamente.")
            continue

        temp_o, viento_o, cielo_o = obtener_clima(lat_origen, lon_origen)
        temp_d, viento_d, cielo_d = obtener_clima(lat_destino, lon_destino)

        print(f"\nNarrativa climática:")
        print(f"En {ciudad_origen} actualmente hay {temp_o:.2f}°C con cielos {cielo_o}, "
              f"y viento de {viento_o:.2f} km/h.")
        print(f"En {ciudad_destino} actualmente hay {temp_d:.2f}°C con cielos {cielo_d}, "
              f"y viento de {viento_d:.2f} km/h.")

if __name__ == "__main__":
    main()
