-- 🐝 Configuración de la Base de Datos
CREATE DATABASE IF NOT EXISTS usda_food;
USE usda_food;

-- 🧹 Eliminar tabla si ya existe para evitar conflictos de metadatos
DROP TABLE IF EXISTS imports_by_country;

-- 📊 Crear Tabla Externa (Apunta directamente a los archivos Parquet de la Capa Gold)
CREATE EXTERNAL TABLE imports_by_country (
    Country STRING,
    TotalValue_MillionUSD DOUBLE
)
STORED AS PARQUET
LOCATION 'hdfs://localhost:9000/datalake/gold/food_imports_by_country'
TBLPROPERTIES ("parquet.compression"="SNAPPY");

-- 🔄 Sincronizar metadatos (Importante si se agregaron archivos nuevos a HDFS)
MSCK REPAIR TABLE imports_by_country;

-- 🔍 Consulta de validación final
-- Formateamos el número para que se vea más limpio en la consola de Hive
SELECT 
    Country, 
    CAST(TotalValue_MillionUSD AS DECIMAL(15,2)) as Millones_USD
FROM imports_by_country 
WHERE Country NOT LIKE '%WORLD%' 
ORDER BY TotalValue_MillionUSD DESC 
LIMIT 5;