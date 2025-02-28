import os
import pandas as pd
import ast

# 📌 Configuración de rutas
base_folder = r"C:\Users\macazella\cvelistV5\cves"
output_folder = r"C:\Users\macazella\CVE_PROJECT"
output_file_corrected = os.path.join(output_folder, "CVE_Unificado_Corregido.csv")

# 📌 Buscar todos los archivos CSV en la carpeta base
csv_files = [f for f in os.listdir(base_folder) if f.endswith(".csv")]

# 📌 Lista para almacenar los DataFrames de cada archivo
dataframes = []

print(f"📂 Se encontraron {len(csv_files)} archivos CSV en {base_folder}")

# 📌 Función para extraer vendor y product de la columna anidada
def extract_vendor_product(json_text):
    try:
        # Convertir el texto en una lista de diccionarios
        affected_list = ast.literal_eval(json_text) if isinstance(json_text, str) else []
        
        # Extraer vendor y product
        vendors = set()
        products = set()
        for item in affected_list:
            if isinstance(item, dict):
                if "vendor" in item:
                    vendors.add(item["vendor"])
                if "product" in item:
                    products.add(item["product"])
        
        # Devolver los valores como strings separados por comas (en caso de múltiples valores)
        return ", ".join(vendors), ", ".join(products)
    
    except Exception:
        return None, None

# 📌 Procesar cada archivo CSV
for file in csv_files:
    file_path = os.path.join(base_folder, file)
    
    try:
        # Cargar el CSV
        df = pd.read_csv(file_path, low_memory=False)
        
        # Verificar si tiene las columnas requeridas
        required_columns = {"cveMetadata.assignerShortName", "cveMetadata.cveId", "cveMetadata.datePublished"}
        if not required_columns.issubset(df.columns):
            print(f"⚠️ {file} omitido: No tiene todas las columnas necesarias.")
            continue

        # Eliminar valores nulos en la fecha
        df = df.dropna(subset=["cveMetadata.datePublished"])

        # Convertir la fecha a formato datetime
        df["cveMetadata.datePublished"] = pd.to_datetime(df["cveMetadata.datePublished"], errors="coerce")

        # Eliminar fechas incorrectas
        df = df.dropna(subset=["cveMetadata.datePublished"])

        # Extraer el año
        df["Año"] = df["cveMetadata.datePublished"].dt.year

        # Extraer cvssBaseScore si existe
        if "containers.cna.x_legacyV4Record.impact.cvss.baseScore" in df.columns:
            df["cvssBaseScore"] = pd.to_numeric(df["containers.cna.x_legacyV4Record.impact.cvss.baseScore"], errors='coerce')

        # Extraer vendor y product si la columna de afectados existe
        if "containers.cna.affected" in df.columns:
            df[["vendor", "product"]] = df["containers.cna.affected"].apply(lambda x: pd.Series(extract_vendor_product(x)))

        # Agregar el DataFrame a la lista
        dataframes.append(df)
        
        print(f"✅ {file} procesado correctamente.")
    except Exception as e:
        print(f"❌ Error procesando {file}: {e}")

# 📌 Unir todos los DataFrames en uno solo
if dataframes:
    df_final = pd.concat(dataframes, ignore_index=True)

    # Seleccionar solo las columnas necesarias para Power BI
    df_final = df_final[["cveMetadata.cveId", "cveMetadata.assignerShortName", "cveMetadata.datePublished", "Año", "cvssBaseScore", "vendor", "product"]]

    # 📌 Guardar el resultado en un CSV
    df_final.to_csv(output_file_corrected, index=False, encoding="utf-8")

    print(f"\n✅ Archivo generado correctamente: {output_file_corrected}")
else:
    print("\n❌ No se pudo generar el archivo final. Revisa los archivos CSV.")
