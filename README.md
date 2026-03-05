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