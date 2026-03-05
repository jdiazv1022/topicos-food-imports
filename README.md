# 📊 FOOD IMPORTS DATA PIPELINE - RESUMEN COMPLETO DEL PROYECTO

## 📋 DESCRIPCIÓN GENERAL DEL PROYECTO

**Nombre:** `topicos-food-imports`  
**Objetivo:** Pipeline completo de ingesta, transformación y análisis de datos de importaciones de alimentos de EE.UU.  
**Arquitectura:** Medallion Architecture (Bronze → Silver → Gold/Functional)  
**Tecnologías Clave:** Apache Spark, Apache Hadoop, Apache Hive, MongoDB, Jenkins, Power BI

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Función |
|-----------|---------|---------|
| **Apache Spark** | 3.5.8 | Procesamiento distribuido |
| **Apache Hadoop** | N/A | Sistema de archivos distribuido (HDFS) |
| **Apache Hive** | 3.x | Data warehouse, análisis SQL |
| **MongoDB** | 5.1.4+ | NoSQL para datos analíticos rápidos |
| **mongo-spark-connector** | 10.4.0 | Conector Spark↔MongoDB |
| **Python** | 3.8+ | Lenguaje de scripting |
| **Jenkins** | N/A | CI/CD (pipeline) |
| **Power BI** | N/A | Visualización (destino final) |
| **Git & GitHub** | N/A | Control de versiones |
| **DBeaver** | N/A | Gestor de bases de datos (Conexión SSH) |

---

## 📂 ESTRUCTURA COMPLETA DEL REPOSITORIO

```
topicos-food-imports/
│
├── 🔧 CONFIGURACIÓN Y CONTROL
│   ├── .git/                       # Control de versiones (Git)
│   ├── .gitignore                  # Archivos ignorados: data/raw, data/processed, venv
│   ├── Jenkinsfile                 # Pipeline CI/CD de Jenkins (vacío actualmente)
│   ├── LICENSE                     # Licencia del proyecto
│   └── README.md                   # Documentación principal (ESTE ARCHIVO)
│
├── ⚙️ CONFIGURACIÓN (config/)
│   └── settings.yaml               # VACÍO - Destinado para rutas HDFS, credenciales, URLs
│
├── 📦 DATOS (data/)
│   ├── raw/                        # DATOS CRUDOS
│   │   └── FoodImports.csv         # 🔴 CSV PRINCIPAL (1.3 MB) - Datos originales sin procesar
│   │
│   └── processed/                  # DATOS PROCESADOS
│       └── [Salida de exportaciones]  # Resultados finales en CSV para Power BI
│
├── 📚 DOCUMENTACIÓN (docs/)
│   ├── diagramas/                  # Imágenes de arquitectura y diagramas
│   └── informe/                    # Informe final del proyecto
│
├── 🗄️ SQL/HIVE (sql/)
│   └── hive/
│       └── create_tables.hql        # Scripts para crear tablas externas en Hive
│
├── 🐍 CÓDIGO FUENTE (src/)
│   ├── ingestion/                  # CAPA BRONZE - Ingesta de datos
│   │   └── bronze_ingestion.py     # VACÍO - Script para cargar CSV a HDFS
│   │
│   ├── processing/                 # CAPAS SILVER y GOLD - Transformación
│   │   ├── silver_transformation.py  # CAPA SILVER ✅ - Limpieza y transformación inicial
│   │   ├── gold_aggregation.py       # CAPA GOLD - VACÍO (agregaciones alternativas)
│   │   └── poblar_capa_functional.py # CAPA FUNCIONAL ✅ - KPIs y agregaciones finales
│   │
│   └── utils/                      # UTILIDADES - Conexiones y exportaciones
│       ├── mongo_connector.py       # VACÍO - Funciones para MongoDB
│       ├── export_gold_to_mongo.py  # ✅ Exportación a MongoDB con Spark
│       ├── export_gold_to_csv.py    # ✅ Exportación a CSV para Power BI
│       └── query_hive.py            # ✅ Consultas SQL en Apache Hive
│
├── 📋 DEPENDENCIAS
│   └── requirements.txt             # VACÍO - Dependencias de Python
│
└── 🔐 ENTORNO
    └── venv/                        # Virtual environment de Python
```

---

## 🔢 ANÁLISIS DETALLADO DE CADA ARCHIVO PYTHON

### **1️⃣ CAPA BRONZE - INGESTA (bronze_ingestion.py)**
**Estado:** ❌ VACÍO  
**Propósito:** Subir el archivo CSV crudo desde el sistema local a HDFS  
**Ubicación esperada:** `/datalake/bronze/food_imports/`

**Comando manual equivalente:**
```bash
hdfs dfs -mkdir -p /datalake/bronze/food_imports
hdfs dfs -put data/raw/FoodImports.csv /datalake/bronze/food_imports/
```

---

### **2️⃣ CAPA SILVER - TRANSFORMACIÓN (silver_transformation.py)**
**Estado:** ✅ IMPLEMENTADO  
**Propósito:** Limpiar y estructurar los datos crudos de Bronze

**Función Principal:** `run_silver_transformation()`

**Operaciones que realiza:**

| Operación | Detalle |
|-----------|---------|
| **Spark Session** | `local[*]` - Usar todos los núcleos disponibles |
| **Input** | HDFS: `hdfs://localhost:9000/datalake/bronze/food_imports/FoodImports.csv` |
| **Casteos** | `YearNum` → INTEGER, `FoodValue` → DOUBLE |
| **Limpieza** | `trim()` en Country, Commodity |
| **Eliminación de nulos** | Remove rows where `FoodValue` o `YearNum` son NULL |
| **Output** | HDFS: `hdfs://localhost:9000/datalake/silver/food_imports` (PARQUET) |

**Columnas procesadas:**
- `YearNum` (Año - Entero)
- `FoodValue` (Valor en millones USD - Decimal)
- `Country` (País proveedor - Texto)
- `Commodity` (Tipo de alimento - Texto)

---

### **3️⃣ CAPA GOLD - AGREGACIONES (poblar_capa_functional.py)**
**Estado:** ✅ IMPLEMENTADO  
**Propósito:** Crear KPIs y agregaciones de negocio

**Función Principal:** `run_functional_layer()`

**KPI 1: VALOR TOTAL POR PAÍS**
```python
df_kpi_country = df_curated.groupBy("Country")
    .agg(round(sum("FoodValue"), 2).alias("TotalValue_MillionUSD"))
    .orderBy(desc("TotalValue_MillionUSD"))
```
**Output:** `hdfs://localhost:9000/datalake/gold/food_imports_by_country`

**Ejemplo de resultado:**
```
+----------------+---------------------+
|         Country|TotalValue_MillionUSD|
+----------------+---------------------+
|WORLD (Quantity)|        2.266484778E7|
|           WORLD|        1.458084541E7|
|   REST OF WORLD|            1160588.7|
|          CANADA|            1025594.4|
|          MEXICO|             967569.1|
+----------------+---------------------+
```

**KPI 2: VALOR POR CATEGORÍA Y AÑO**
```python
df_kpi_category_year = df_curated.groupBy("YearNum", "Category")
    .agg(round(sum("FoodValue"), 2).alias("YearlyValue_MillionUSD"))
    .orderBy("YearNum", desc("YearlyValue_MillionUSD"))
```
**Output:** `hdfs://localhost:9000/datalake/gold/food_imports_by_category`

**Configuración Spark:**
- Compresión: Snappy (más rápido que gzip)
- Formato: Parquet (optimizado para consultas analíticas)

---

### **4️⃣ EXPORTACIÓN A MONGO (export_gold_to_mongo.py)**
**Estado:** ✅ IMPLEMENTADO (pero requiere MongoDB corriendo)  
**Propósito:** Migrar datos de Capa Gold a MongoDB para consultas rápidas

**Función Principal:** `export_to_mongo()`

**Pasos de ejecución:**

| Paso | Descripción |
|------|-------------|
| 1️⃣ | Inicializar SparkSession en `local[*]` |
| 2️⃣ | Leer PARQUET de HDFS: `/datalake/gold/food_imports_by_country` |
| 3️⃣ | Conectar a MongoDB en `127.0.0.1:27017` |
| 4️⃣ | Escribir en BD `usda_food`, colección `imports_by_country` |
| 5️⃣ | Modo: OVERWRITE (reemplazar colección existente) |

**Parámetros de Conexión:**
```python
.option("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1:27017/")
.option("database", "usda_food")
.option("collection", "imports_by_country")
```

**Dependencia:** `--packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0`

---

### **5️⃣ EXPORTACIÓN A CSV (export_gold_to_csv.py)**
**Estado:** ✅ IMPLEMENTADO  
**Propósito:** Exportar datos Gold a CSV para Power BI

**Función Principal:** `export_to_csv()`

**Pasos:**
1. Leer PARQUET: `/datalake/gold/food_imports_by_country`
2. Usar `coalesce(1)` para generar UN SOLO archivo .csv
3. Guardar en: `file:/home/hadoop/topicos-food-imports/data/processed/gold_export`
4. Incluir headers (encabezados)

---

### **6️⃣ CONSULTAS EN HIVE (query_hive.py)**
**Estado:** ✅ IMPLEMENTADO  
**Propósito:** Consultar datos con SQL en Apache Hive

**Función Principal:** `query_hive()`

**SQL ejecutado:**
```sql
USE usda_food;

SELECT 
    Country as Pais_Origen, 
    CAST(TotalValue_MillionUSD AS DECIMAL(15,2)) as Millones_USD
FROM imports_by_country 
WHERE Country NOT LIKE '%WORLD%' 
ORDER BY TotalValue_MillionUSD DESC 
LIMIT 5
```

**Lo que hace:**
- Selecciona TOP 5 países por valor de importación
- Excluye registros con "WORLD" en el nombre
- Formatea valores a DECIMAL(15,2)
- Ordena descendente por valor

---

### **7️⃣ SQL HIVE - DDL (create_tables.hql)**
**Estado:** ✅ IMPLEMENTADO  
**Propósito:** Crear tablas externas en Hive apuntando a datos Gold

**Script SQL:**
```sql
CREATE DATABASE IF NOT EXISTS usda_food;
USE usda_food;

CREATE EXTERNAL TABLE IF NOT EXISTS imports_by_country (
    Country STRING,
    TotalValue_MillionUSD DOUBLE
)
STORED AS PARQUET
LOCATION 'hdfs://localhost:9000/datalake/gold/food_imports_by_country';
```

**Detalles:**
- **Tipo:** EXTERNAL - Los archivos están en HDFS
- **Formato:** PARQUET (comprimido, optimizado)
- **Localización:** Apunta a carpeta HDFS de Capa Gold
- **Columnas:** Country (texto), TotalValue_MillionUSD (decimal)

---

## 🔄 FLUJO DE DATOS COMPLETO

```
                    PIPELINE DATA LAKEHOUSE
                    
┌────────────────────────────────────────────────┐
│  FoodImports.csv (1.3 MB)                     │
│  En: data/raw/                                │
└──────────────┬─────────────────────────────────┘
               │
               │ bronze_ingestion.py
               │ hdfs dfs -put
               ▼
┌────────────────────────────────────────────────┐
│  🔴 CAPA BRONZE (Raw/Crudo)                   │
│  /datalake/bronze/food_imports/               │
│  ❌ Sin transformación                        │
└──────────────┬─────────────────────────────────┘
               │
               │ silver_transformation.py ✅
               │ • Casteo de tipos
               │ • Limpieza (trim, dropna)
               │ • Formato Parquet
               ▼
┌────────────────────────────────────────────────┐
│  🟡 CAPA SILVER (Curated/Limpio)              │
│  /datalake/silver/food_imports/               │
│  ✅ Datos estructurados, sin nulos            │
└──────────────┬─────────────────────────────────┘
               │
               │ poblar_capa_functional.py ✅
               │ • Agregaciones por país
               │ • Agregaciones por categoría/año
               │ • KPIs de negocio
               ▼
┌────────────────────────────────────────────────┐
│  🟢 CAPA GOLD/FUNCIONAL (Analytical)          │
│  ├── /datalake/gold/food_imports_by_country  │
│  └── /datalake/gold/food_imports_by_category │
│  ✅ Datos agregados, listos para consumo      │
└────┬──────────────────────────┬───────────────┘
     │                          │
┌────▼────────┐        ┌────────▼────┐
│ export_gold_│        │query_hive.py│
│_to_csv.py✅ │        │      ✅     │
│ → CSV       │        │SQL Queries  │
└────┬────────┘        └─────────────┘
     │
     ▼
┌────────────────────┐    ┌──────────────────┐
│   POWER BI 📊      │    │ MongoDB 🍃      │
│  /data/processed/  │    │ export_gold_    │
│ Visualización      │    │ to_mongo.py ✅  │
└────────────────────┘    └──────────────────┘
```

---

## 🚀 GUÍA DE EJECUCIÓN PASO A PASO

### 1. Requisitos Previos

Asegúrate de tener corriendo los servicios en tu entorno WSL:

```bash
start-dfs.sh
start-yarn.sh
hive --service metastore &
hive --service hiveserver2 &
```

### 2. Ingesta de Datos (Capa Bronze)

```bash
hdfs dfs -mkdir -p /datalake/bronze/food_imports
hdfs dfs -put ~/topicos-food-imports/data/raw/FoodImports.csv /datalake/bronze/food_imports/
```

### 3. Procesamiento con PySpark (Capas Silver y Gold)

```bash
# Capa Silver - Limpieza
spark-submit src/processing/silver_transformation.py

# Capa Gold/Funcional - Agregaciones
spark-submit src/processing/poblar_capa_functional.py
```

### 4. Exportación a CSV (para Power BI)

```bash
spark-submit src/utils/export_gold_to_csv.py
```

### 5. Consultas con Hive

```bash
# Crear tablas externas
hive -f sql/hive/create_tables.hql

# Ejecutar consultas SQL
spark-submit src/utils/query_hive.py

# O consultar directamente en Hive
hive -e "USE usda_food; SELECT * FROM imports_by_country LIMIT 5;"
```

### 6. Persistencia en MongoDB (Opcional - Requiere MongoDB)

```bash
# Opción 1: Iniciar MongoDB con Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Opción 2: Iniciar MongoDB manualmente (si está instalado)
mongod --dbpath /data/db &

# Ejecutar exportación a MongoDB
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0 \
  src/utils/export_gold_to_mongo.py
```

### 7. Integración Continua (Jenkins)

Cualquier push a la rama `main` en GitHub disparará automáticamente el pipeline configurado en `Jenkinsfile`.

---

## 📊 DATOS PRINCIPALES

### **Archivo de Entrada:**
- **Nombre:** `FoodImports.csv`
- **Ubicación:** `data/raw/`
- **Tamaño:** 1.3 MB (1,372,240 bytes)
- **Formato:** CSV con headers
- **Ruta HDFS:** `/datalake/bronze/food_imports/FoodImports.csv`

### **Columnas esperadas:**
```
YearNum       - Año (entero)
Country       - País de origen (texto)
Commodity     - Tipo de alimento (texto)
FoodValue     - Valor importado en millones USD (decimal)
Category      - Categoría de alimento (texto)
```

---

## ✅/❌ ESTADO DE IMPLEMENTACIÓN

| Archivo | Estado | Descripción |
|---------|--------|-------------|
| `bronze_ingestion.py` | ❌ VACÍO | Necesaria implementación |
| `silver_transformation.py` | ✅ COMPLETO | Limpieza funcionando |
| `gold_aggregation.py` | ❌ VACÍO | Similar a poblar_capa_functional.py |
| `poblar_capa_functional.py` | ✅ COMPLETO | KPIs generados |
| `export_gold_to_mongo.py` | ⚠️ COMPLETO | Requiere MongoDB en ejecución |
| `export_gold_to_csv.py` | ✅ COMPLETO | Exportación a CSV lista |
| `query_hive.py` | ✅ COMPLETO | Consultas SQL funcionando |
| `create_tables.hql` | ✅ COMPLETO | Tablas externas creadas |
| `mongo_connector.py` | ❌ VACÍO | Utilidad sin usar |
| `requirements.txt` | ❌ VACÍO | Dependencias no listadas |
| `settings.yaml` | ❌ VACÍO | Configuración no documentada |
| `Jenkinsfile` | ❌ VACÍO | CI/CD no configurado |

---

## 📝 RESUMEN EJECUTIVO

Tu proyecto es un **Data Lake completo con arquitectura Medallion (Bronze-Silver-Gold)** que:

1. **Ingesta 🥕** - Carga CSV de importaciones de alimentos
2. **Transforma ✨** - Limpia datos en capa Silver
3. **Agrega 📊** - Genera KPIs en capa Gold
4. **Visualiza 📈** - Exporta a CSV para Power BI
5. **Queries 🐝** - Permite SQL avanzado en Hive
6. **NoSQL 🍃** - Integración con MongoDB para acceso rápido

**Pipeline funcional:** ✅ Sí (hasta CSV)  
**Archivos implementados:** 6/10 (60%)  

---

## 👥 Equipo de Trabajo

* **Maycol Mondragon**
* **Jaime Diaz**
* **Jhoel Lanos**

---

**Última actualización:** March 5, 2026



