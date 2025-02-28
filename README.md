# Analisis_Vulnerabilidades_CVE
"Análisis de vulnerabilidades CVE reportadas en 2024 y 2025 con visualización en Power BI."
🔹 1. Objetivo del Proyecto

El análisis busca identificar tendencias en la cantidad de vulnerabilidades reportadas (CVEs) en los años 2024 y 2025, destacando los fabricantes y productos más afectados. Se emplearon herramientas de Power BI para la visualización de datos y Python para el procesamiento y transformación de los mismos.

🔹 2. Fuentes de Datos y Transformaciones

📁 Dataset Utilizado:

✅ CVE_Unificado_Corregido.csv → Base de datos consolidada con CVEs reportados en 2024 y 2025.

📌 Fuente de Datos Original

Los datos de vulnerabilidades CVE fueron obtenidos desde la fuente oficial de la National Vulnerability Database (NVD):
🔗 https://nvd.nist.gov/vuln/data-feeds

Desde este portal, se descargan los archivos JSON con los registros de vulnerabilidades, los cuales luego son procesados y normalizados para su análisis en Power BI.

📌 Pasos del ETL (Extract, Transform, Load)

🔹 1. Extracción de Datos

Se extrajeron los datos en formato JSON y se transformaron en CSV para su análisis en Power BI.

Script utilizado: extraer_cve_por_anio.py

🔹 2. Limpieza y Normalización

Se eliminaron duplicados y se corrigieron inconsistencias en los datos de fabricantes y productos.

Script utilizado: etl_cve_processing.py

🔹 3. Consolidación y Creación del Archivo Final

Se fusionaron los datos en una única tabla (CVE_Unificado_Corregido.csv).

Este dataset final es la base de las visualizaciones en Power BI.


🔹 3. Visualización en Power BI

✅ Se crearon gráficos para facilitar el análisis de tendencias:

Barras: CVEs reportados por empresa.

Línea temporal: Evolución de CVEs por mes.

Matriz: Distribución de CVEs por fabricante y producto.

Treemap: Empresas y productos con más vulnerabilidades reportadas.

🔍 Corrección realizada: Se detectó que algunos gráficos no reflejaban correctamente la distribución de CVEs, por lo que se revisó y ajustó el dataset en Power BI.

📂 Archivos subidos al repositorio:
✅ Dashboard_CVEs.pbix (Power BI con el análisis completo)
✅ Informe_Analisis_CVEs.pdf (Presentación en PDF)
