from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower

def run_silver_transformation():
    # 1. Iniciar la sesión de Spark
    spark = SparkSession.builder \
        .appName("FoodImports_SilverLayer") \
        .master("local[*]") \
        .getOrCreate()

    print("--- Iniciando Transformación Capa Silver ---")

    # 2. Leer los datos crudos desde la Capa Bronze en HDFS
    bronze_path = "hdfs://localhost:9000/datalake/bronze/food_imports/FoodImports.csv"
    
    df_bronze = spark.read.csv(bronze_path, header=True, inferSchema=True)

    # 3. Limpieza y Transformación (Capa Silver)
    # - Castear tipos de datos correctamente
    # - Eliminar espacios en blanco
    df_silver = df_bronze \
        .withColumn("YearNum", col("YearNum").cast("integer")) \
        .withColumn("FoodValue", col("FoodValue").cast("double")) \
        .withColumn("Country", trim(col("Country"))) \
        .withColumn("Commodity", trim(col("Commodity"))) \
        .dropna(subset=["FoodValue", "YearNum"]) # Eliminar nulos en columnas clave

    # 4. Mostrar esquema y un par de filas para validar
    df_silver.printSchema()
    df_silver.show(5)

    # 5. Guardar los datos limpios en la Capa Silver como formato Parquet
    silver_path = "hdfs://localhost:9000/datalake/silver/food_imports"
    df_silver.write.mode("overwrite").parquet(silver_path)

    print(f"--- Datos guardados exitosamente en formato Parquet en: {silver_path} ---")
    spark.stop()

if __name__ == "__main__":
    run_silver_transformation()