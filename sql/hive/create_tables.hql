-- 🐝 Crear Base de Datos
CREATE DATABASE IF NOT EXISTS usda_food;
USE usda_food;

-- 📊 Crear Tabla Externa
CREATE EXTERNAL TABLE IF NOT EXISTS imports_by_country (
    Country STRING,
    TotalValue_MillionUSD DOUBLE
)
STORED AS PARQUET
LOCATION 'hdfs://localhost:9000/datalake/gold/food_imports_by_country';

-- 🔍 Consulta de prueba (La tabla final mostrará CANADA, MEXICO, ITALY, etc.)
SELECT * FROM imports_by_country ORDER BY TotalValue_MillionUSD DESC LIMIT 5;