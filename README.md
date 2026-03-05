* **Base de Datos NoSQL:** MongoDB
* **Orquestación / CI/CD:** Jenkins (Pipelines automatizados)
* **Gestor de Base de Datos:** DBeaver (Conexión SSH)
* **Visualización:** Power BI
* **Control de Versiones:** Git & GitHub

## 📂 Estructura del Repositorio
\`\`\`text

topicos-food-imports/
│
├── .git/                       # Carpeta oculta de control de versiones
├── .gitignore                  # Archivos que GitHub debe ignorar (ej. carpetas /data o archivos .csv pesados)
├── README.md                   # Documentación principal para tu equipo (cómo ejecutar el código)
├── requirements.txt            # Dependencias de Python (ej. pyspark, pymongo)
├── Jenkinsfile                 # Pipeline de Jenkins para la integración continua (Capítulo 9) 
│
├── config/
│   └── settings.yaml           # Rutas a HDFS, credenciales de Mongo, URLs (evita poner texto duro en el código)
│
├── data/                       # (No subir a GitHub si pesa mucho, añadir a .gitignore)
│   ├── raw/                    # Aquí colocas el CSV descargado de "U.S. Food Imports" original
│   └── processed/              # Muestras locales de datos procesados (opcional)
│
├── docs/
│   ├── informe/                # El documento Word del Informe Final y prototipos de Figma [cite: 184]
│   └── diagramas/              # Imágenes de la arquitectura y capturas para los Anexos [cite: 218, 223]
│
├── sql/
│   └── hive/
│       └── create_tables.hql   # Scripts SQL para crear las tablas en Hive apuntando a la capa Gold [cite: 171]
│
└── src/                        # Código fuente del proyecto
    ├── ingestion/
    │   └── bronze_ingestion.py # Script para subir el CSV crudo al HDFS (/datalake/bronze) [cite: 146]
    │
    ├── processing/
    │   ├── silver_transformation.py # PySpark: Limpieza, manejo de nulos y duplicados (Capítulo 5) [cite: 161, 163, 164]
    │   └── gold_aggregation.py      # PySpark: Agregaciones, KPIs de negocio y cálculos finales [cite: 166]
    │
    └── utils/
        └── mongo_connector.py       # Funciones auxiliares para conectar y enviar la capa Gold a MongoDB [cite: 177]



\`\`\`

## 🚀 Guía de Ejecución Paso a Paso

### 1. Requisitos Previos
Asegúrate de tener corriendo los servicios en tu entorno WSL:
\`\`\`bash
start-dfs.sh
start-yarn.sh
hive --service metastore &
hive --service hiveserver2 &
\`\`\`

### 2. Ingesta de Datos (Capa Bronze)
Sube el archivo CSV crudo a HDFS mediante la terminal o ejecutando el script de ingesta:
\`\`\`bash
hdfs dfs -mkdir -p /datalake/bronze/food_imports
hdfs dfs -put data/raw/food_imports.csv /datalake/bronze/food_imports/
\`\`\`

### 3. Procesamiento con PySpark (Capas Silver y Gold)
Ejecuta los scripts de transformación para limpiar los datos y generar los KPIs:
\`\`\`bash
spark-submit src/processing/silver_transformation.py
spark-submit src/processing/gold_aggregation.py
\`\`\`

### 4. Consultas con Hive y DBeaver
Conéctate a Hive a través de DBeaver (usando túnel SSH al puerto `10000` de tu WSL). Ejecuta el script `sql/hive/create_tables.hql` para crear las tablas externas apuntando a los archivos Parquet de la capa Gold.

### 5. Persistencia en MongoDB
El script de la capa Gold automáticamente escribirá una colección final en MongoDB para consumo rápido utilizando el conector `mongo-spark-connector`.

### 6. Integración Continua (Jenkins)
Cualquier *push* realizado a la rama `main` en este repositorio de GitHub disparará automáticamente el pipeline configurado en Jenkins (`Jenkinsfile`), el cual validará el código y ejecutará los jobs de PySpark.

## 👥 Equipo de Trabajo
* **[Tu Nombre]** - Arquitectura de Datos y PySpark
* **[Nombre Integrante 2]** - Ingesta, Hive y Jenkins
* **[Nombre Integrante 3]** - MongoDB, Power BI y Documentación
*(Nota: Ajustar roles según la participación real de cada integrante)*