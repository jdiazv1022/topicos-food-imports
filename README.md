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
| **Apache Hadoop** | 3.x | Sistema de archivos distribuido (HDFS) |
| **Apache Hive** | 3.x | Data warehouse, análisis SQL |
| **MongoDB** | 8.x | NoSQL para datos analíticos rápidos |
| **mongo-spark-connector** | 10.4.0 | Conector Spark↔MongoDB |
| **Python** | 3.8+ | Lenguaje de scripting |
| **Jenkins** | N/A | Orquestación CI/CD (pipeline automatizado) |
| **Power BI** | N/A | Visualización (destino final) |
| **Git & GitHub** | N/A | Control de versiones |
| **DBeaver** | N/A | Gestor de bases de datos (Conexión SSH) |

---

## 📂 ESTRUCTURA COMPLETA DEL REPOSITORIO

```text
topicos-food-imports/
│
├── 🔧 CONFIGURACIÓN Y CONTROL
│   ├── .git/                       # Control de versiones (Git)
│   ├── .gitignore                  # Archivos ignorados: data/raw, data/processed, venv
│   ├── Jenkinsfile                 # ✅ Pipeline CI/CD declarativo configurado y funcional
│   ├── LICENSE                     # Licencia del proyecto
│   └── README.md                   # Documentación principal (ESTE ARCHIVO)
│
├── ⚙️ CONFIGURACIÓN (config/)
│   └── settings.yaml               # ✅ Archivo centralizado de rutas HDFS y credenciales
│
├── 📦 DATOS (data/)
│   ├── raw/                        # DATOS CRUDOS
│   │   └── FoodImports.csv         # 🔴 CSV PRINCIPAL (1.3 MB) - Datos originales sin procesar
│   │
│   └── processed/                  # DATOS PROCESADOS
│       └── gold_export/            # ✅ Resultados finales en CSV para Power BI
│
├── 📚 DOCUMENTACIÓN (docs/)
│   ├── diagramas/                  # Imágenes de arquitectura y diagramas (Anexos)
│   └── informe/                    # Informe final del proyecto
│
├── 🗄️ SQL/HIVE (sql/)
│   └── hive/
│       └── create_tables.hql       # ✅ Scripts DDL para crear tablas externas en Hive
│
├── 🐍 CÓDIGO FUENTE (src/)
│   ├── ingestion/                  # CAPA BRONZE - Ingesta de datos
│   │   └── bronze_ingestion.py     # ✅ Script PySpark para cargar CSV a HDFS automáticamente
│   │
│   ├── processing/                 # CAPAS SILVER y GOLD - Transformación
│   │   ├── silver_transformation.py  # ✅ CAPA SILVER - Limpieza, casteo y filtros de calidad
│   │   ├── gold_aggregation.py       # ✅ CAPA GOLD - Agregaciones extra (Promedios por categoría)
│   │   └── poblar_capa_functional.py # ✅ CAPA FUNCIONAL - KPIs principales de negocio
│   │
│   └── utils/                      # UTILIDADES - Conexiones y exportaciones
│       ├── mongo_connector.py        # ✅ Lector de configuración YAML dinámico
│       ├── export_gold_to_mongo.py   # ✅ Exportación a MongoDB con Spark
│       ├── export_gold_to_csv.py     # ✅ Exportación unificada a CSV para Power BI
│       └── query_hive.py             # ✅ Consultas SQL en Apache Hive vía Spark
│
├── 📋 DEPENDENCIAS
│   └── requirements.txt             # ✅ Dependencias oficiales de Python (pyspark, pymongo, etc.)
│
└── 🔐 ENTORNO
    └── venv/                        # Virtual environment de Python

```

---

## 🔢 ANÁLISIS DETALLADO DE CADA ARCHIVO PYTHON

### **1️⃣ CAPA BRONZE - INGESTA (bronze_ingestion.py)**

**Estado:** ✅ IMPLEMENTADO

**Propósito:** Automatizar la subida del archivo CSV crudo desde el sistema local a HDFS mediante PySpark.

**Ubicación de destino:** `/datalake/bronze/food_imports/`

---

### **2️⃣ CAPA SILVER - TRANSFORMACIÓN (silver_transformation.py)**

**Estado:** ✅ IMPLEMENTADO

**Propósito:** Limpiar, estructurar y aplicar Gobernanza/Calidad a los datos crudos.

**Operaciones de Calidad (Data Quality):**

* **Casteos:** `YearNum` → INTEGER, `FoodValue` → DOUBLE
* **Limpieza:** `trim()` y `upper()` en Country
* **Eliminación de Nulos:** Se descartan filas vacías en métricas clave (`dropna`).
* **Filtros de Anomalías:** Eliminación estricta de totales globales (ej. `"WORLD"`, `"REST OF WORLD"`).
* **Filtro de Unidades:** Solo se procesan filas financieras (`UOM == "Million $"`), descartando toneladas.
* **Output:** HDFS `/datalake/silver/food_imports` (Formato **PARQUET** comprimido con **Snappy**).

---

### **3️⃣ CAPA GOLD - AGREGACIONES (poblar_capa_functional.py y gold_aggregation.py)**

**Estado:** ✅ IMPLEMENTADO

**Propósito:** Crear Data Marts analíticos y KPIs orientados al negocio.

**Métricas Calculadas:**

1. **Valor Total Histórico por País:** Identificación precisa del Top de proveedores (ej. Canadá, México).
2. **Valor por Categoría y Año:** Evolución temporal de las importaciones.
3. **Promedio de Valor por Categoría:** Cálculo estadístico en archivo secundario.
**Output:** Rutas separadas en `/datalake/gold/...` (Formato Parquet).

---

### **4️⃣ EXPORTACIÓN A MONGO (export_gold_to_mongo.py)**

**Estado:** ✅ IMPLEMENTADO

**Propósito:** Migrar la Capa Gold a MongoDB (Local/Windows) para consultas de baja latencia.

**Detalles Técnicos:**

* **Conexión:** `mongodb://127.0.0.1:27017/`
* **Destino:** Base de datos `usda_food`, colección `imports_by_country`.
* **Modo:** `OVERWRITE`.

---

### **5️⃣ EXPORTACIÓN A CSV (export_gold_to_csv.py)**

**Estado:** ✅ IMPLEMENTADO

**Propósito:** Consolidar datos de la Capa Gold a un solo archivo CSV usando `coalesce(1)` para facilitar la importación en tableros de **Power BI**.

---

### **6️⃣ CONSULTAS EN HIVE (query_hive.py y create_tables.hql)**

**Estado:** ✅ IMPLEMENTADO

**Propósito:** Consultas SQL avanzadas en Data Warehouse.

* **DDL (`create_tables.hql`):** Crea la base de datos `usda_food` y la tabla `EXTERNAL` apuntando a los archivos Parquet en HDFS.
* **Consultas (`query_hive.py`):** Utiliza Spark SQL conectado al Metastore de Hive para realizar selects formateados y ordenados.

---

## 🔄 FLUJO DE DATOS COMPLETO

```text
                    PIPELINE DATA LAKEHOUSE
                    
┌────────────────────────────────────────────────┐
│  FoodImports.csv (1.3 MB)                      │
│  En: data/raw/                                 │
└──────────────┬─────────────────────────────────┘
               │
               │ bronze_ingestion.py ✅
               ▼
┌────────────────────────────────────────────────┐
│  🔴 CAPA BRONZE (Raw/Crudo)                    │
│  /datalake/bronze/food_imports/                │
│  ✅ Ingesta automatizada con PySpark           │
└──────────────┬─────────────────────────────────┘
               │
               │ silver_transformation.py ✅
               │ • Filtro estricto de nulos y anomalías
               │ • Formato Parquet + Snappy
               ▼
┌────────────────────────────────────────────────┐
│  🟡 CAPA SILVER (Curated/Limpio)               │
│  /datalake/silver/food_imports/                │
│  ✅ Datos 100% estructurados y limpios         │
└──────────────┬─────────────────────────────────┘
               │
               │ poblar_capa_functional.py ✅
               │ gold_aggregation.py ✅
               ▼
┌────────────────────────────────────────────────┐
│  🟢 CAPA GOLD/FUNCIONAL (Analytical)           │
│  ├── /datalake/gold/food_imports_by_country    │
│  └── /datalake/gold/food_imports_by_category   │
│  ✅ Datos agregados, listos para consumo       │
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
│   POWER BI 📊      │    │ MongoDB 🍃       │
│  /data/processed/  │    │ export_gold_     │
│ Visualización      │    │ to_mongo.py ✅   │
└────────────────────┘    └──────────────────┘

```

---

## 🚀 GUÍA DE EJECUCIÓN PASO A PASO

### 1. Iniciar Servicios

Asegúrate de tener corriendo los servicios en tu entorno WSL y Windows:

```bash
start-dfs.sh
start-yarn.sh
hive --service metastore &
hive --service hiveserver2 &
sudo systemctl start mongod  # (O MongoDB Desktop en Windows)

```

### 2. Ejecutar Pipeline PySpark (Bronze, Silver y Gold)

```bash
# Capa Bronze - Ingesta automatizada
spark-submit src/ingestion/bronze_ingestion.py

# Capa Silver - Limpieza y Gobernanza
spark-submit src/processing/silver_transformation.py

# Capa Gold/Funcional - Agregaciones y KPIs
spark-submit src/processing/poblar_capa_functional.py
spark-submit src/processing/gold_aggregation.py

```

### 3. Distribución a Sistemas de Consumo

```bash
# Exportar consolidado a CSV (Para Power BI)
spark-submit src/utils/export_gold_to_csv.py

# Exportar a Base de Datos NoSQL (MongoDB)
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0 src/utils/export_gold_to_mongo.py

# Crear esquema y consultar analítica en Hive
hive -f sql/hive/create_tables.hql
spark-submit src/utils/query_hive.py

```

### 4. Integración Continua (Jenkins)

Cualquier evento `git push` a la rama principal de GitHub disparará automáticamente la ejecución orquestada en Jenkins leyendo el `Jenkinsfile`.

---

## ✅ ESTADO DE IMPLEMENTACIÓN FINAL

| Archivo | Estado | Descripción |
| --- | --- | --- |
| `bronze_ingestion.py` | ✅ COMPLETO | Ingesta automatizada hacia HDFS configurada |
| `silver_transformation.py` | ✅ COMPLETO | Limpieza robusta y calidad de datos aplicada |
| `gold_aggregation.py` | ✅ COMPLETO | Agregaciones secundarias completadas |
| `poblar_capa_functional.py` | ✅ COMPLETO | KPIs principales generados correctamente |
| `export_gold_to_mongo.py` | ✅ COMPLETO | Migración nativa a MongoDB validada |
| `export_gold_to_csv.py` | ✅ COMPLETO | Generación de archivo maestro para Dashboards |
| `query_hive.py` | ✅ COMPLETO | Consultas SQL vía Spark ejecutadas sin errores |
| `create_tables.hql` | ✅ COMPLETO | Tablas externas (DDL) mapeadas a la Capa Gold |
| `mongo_connector.py` | ✅ COMPLETO | Utilidad de lectura de archivos YAML funcional |
| `requirements.txt` | ✅ COMPLETO | Dependencias y librerías declaradas |
| `settings.yaml` | ✅ COMPLETO | Variables de entorno centralizadas |
| `Jenkinsfile` | ✅ COMPLETO | Pipeline declarativo CI/CD 100% operativo |

---

## 📝 RESUMEN EJECUTIVO (100% LOGRADO)

Tu proyecto es un **Data Lakehouse de nivel empresarial con arquitectura Medallion** totalmente automatizado que:

1. **Ingesta 🥕** - Orquesta la subida de datos crudos a HDFS.
2. **Transforma ✨** - Garantiza Gobernanza y Calidad en la Capa Silver.
3. **Agrega 📊** - Genera Data Marts precisos en Capa Gold.
4. **Visualiza 📈** - Alimenta tableros dinámicos en Power BI.
5. **Queries 🐝** - Ejecuta DDL y SQL avanzado en Apache Hive.
6. **NoSQL 🍃** - Sincroniza KPIs con MongoDB para lectura rápida.
7. **CI/CD 🤖** - Automatiza tareas de integración con Jenkins.

**Pipeline funcional:** ✅ Sí (End-to-End validado)

**Archivos implementados:** 12/12 (100%)

---

## 👥 Equipo de Trabajo

* **Maycol Mondragon**
* **Jaime Diaz**
* **Jhoel Llanos**

---

**Última actualización:** 5 de Marzo, 2026

