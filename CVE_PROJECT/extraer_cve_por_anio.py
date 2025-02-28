import os
import json
import pandas as pd
from multiprocessing import Pool, cpu_count

# Configuración de rutas
base_folder = r"C:\Users\macazella\cvelistV5\cves"
output_folder = r"C:\Users\macazella\cvelistV5\procesados"
os.makedirs(output_folder, exist_ok=True)  # Crear carpeta si no existe

years = ["2024", "2025"]  # Años a procesar
num_workers = min(cpu_count(), 4)  # Usa 4 procesos en paralelo

def process_json_file(filepath, year):
    """Función para leer y procesar un archivo JSON"""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            data["año"] = year
            return data
    except json.JSONDecodeError:
        print(f"⚠️ Error al leer {filepath}")
        return None

def process_year(year):
    """Procesa todos los archivos JSON de un año"""
    json_folder = os.path.join(base_folder, year)
    if not os.path.exists(json_folder):
        print(f"❌ La carpeta {json_folder} no existe. Saltando...")
        return

    file_list = []
    for subdir in os.listdir(json_folder):
        subdir_path = os.path.join(json_folder, subdir)
        if os.path.isdir(subdir_path):
            for filename in os.listdir(subdir_path):
                if filename.endswith(".json"):
                    file_list.append(os.path.join(subdir_path, filename))

    print(f"📌 Procesando {len(file_list)} archivos de {year} usando {num_workers} núcleos...")

    # Multiprocesamiento: divide la carga de trabajo
    with Pool(processes=num_workers) as pool:
        results = pool.starmap(process_json_file, [(f, year) for f in file_list])

    # Filtrar registros válidos
    results = [r for r in results if r is not None]

    # Guardar como CSV
    if results:
        df = pd.json_normalize(results)
        output_csv = os.path.join(output_folder, f"cve_{year}.csv")
        df.to_csv(output_csv, index=False, encoding="utf-8")
        print(f"✅ Archivo guardado: {output_csv} ({len(results)} registros)")
    else:
        print(f"⚠️ No se encontraron datos procesables para {year}")

if __name__ == "__main__":
    for year in years:
        process_year(year)

