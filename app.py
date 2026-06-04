import csv
import requests
from bs4 import BeautifulSoup

def obtener_html(url):
    """
    Función para obtener el contenido HTML de una página web.
    Parámetros:
        - url: La URL de la página web a obtener.
    Retorna: El contenido HTML de la página web si la solicitud es exitosa, o None si hay un error
    """
    try:
        # Configurar un User-Agent para evitar bloqueos por parte del servidor
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error al obtener la página: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error al obtener la página: {e}")
        return None
    
def extraer_datos(html):
    """
    Función para extraer datos específicos del contenido HTML utilizando BeautifulSoup.
    Parámetros:
        - html: El contenido HTML de la página web.
    Retorna: Una lista de diccionarios con los datos extraídos.
    """
    soup = BeautifulSoup(html, "html.parser")
    datos = []
    counter = 1
    for item in soup.find_all("div", class_="contenedor-titulo"): # "div", class_="contenedor-titulo"): ##ucHomePage_cuNoticiaDeporte_repNoticiaDeporteSec_cajaCont_2 > div.contenedor-titulo
        titulo = item.text.strip()
        hipervinculo = item.find("a")["href"] if item.find("a") else "Sin enlace"
        datos.append({"titulo": titulo, "hipervinculo": hipervinculo})
        print(f"{counter} - Titulo: {titulo}\nHipervínculo: {hipervinculo}")
        counter += 1
    
    return datos    

url = "https://www.emol.com/"
html = obtener_html(url)
if html:
    datos = extraer_datos(html)
    # Guardar los datos en un archivo CSV
    with open("datos.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["titulo", "hipervinculo"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for dato in datos:
            writer.writerow(dato)
    print("Datos guardados en datos.csv")