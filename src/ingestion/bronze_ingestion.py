import os
from pyspark.sql import SparkSession

def run_bronze_ingestion():
    spark = SparkSession.builder \
        .appName("FoodImports_BronzeIngestion") \
        .master("local[*]") \
        .getOrCreate()

    print("--- 🥉 Iniciando Ingesta a Capa Bronze ---")

    # Ruta dinámica para leer el CSV local
    current_dir = os.getcwd()
    local_path = f"file://{current_dir}/data/raw/FoodImports.csv"
    bronze_path = "hdfs://localhost:9000/datalake/bronze/food_imports"
    
    try:
        # Leer el CSV crudo
        df_raw = spark.read.csv(local_path, header=True, inferSchema=True)
        print(f"✅ Archivo local leído. Total de registros: {df_raw.count()}")
        
        # Guardar en HDFS tal cual (crudo)
        df_raw.write.mode("overwrite").csv(bronze_path, header=True)
        print(f"✅ Datos ingestados con éxito en HDFS: {bronze_path}")
        
    except Exception as e:
        print(f"❌ Error en la ingesta: {e}")
        
    spark.stop()

if __name__ == "__main__":
    run_bronze_ingestion()