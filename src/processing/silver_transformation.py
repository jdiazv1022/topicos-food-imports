from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper

def run_silver_transformation():
    # 1. Iniciar la sesión de Spark
    spark = SparkSession.builder \
        .appName("FoodImports_SilverLayer") \
        .master("local[*]") \
        .getOrCreate()

    print("--- 🥈 Iniciando Transformación Capa Silver ---")

    # 2. Leer los datos crudos
    bronze_path = "hdfs://localhost:9000/datalake/bronze/food_imports"
    df_bronze = spark.read.csv(bronze_path, header=True, inferSchema=True)

    # 3. Limpieza Estricta y Filtros de Calidad
    df_silver = df_bronze \
        .withColumn("YearNum", col("YearNum").cast("integer")) \
        .withColumn("FoodValue", col("FoodValue").cast("double")) \
        .withColumn("Country", trim(upper(col("Country")))) \
        .withColumn("Commodity", trim(col("Commodity"))) \
        .dropna(subset=["FoodValue", "YearNum", "Country"]) \
        .filter(~col("Country").isin("WORLD (QUANTITY)", "WORLD", "REST OF WORLD")) \
        .filter(col("UOM") == "Million $") # CRÍTICO: Descarta toneladas, conserva solo dinero

    # 4. Validar resultados
    print("📊 Muestra de datos limpios (Solo países reales y montos en USD):")
    df_silver.printSchema()
    df_silver.show(5, truncate=False)

    # 5. Guardar en Parquet
    silver_path = "hdfs://localhost:9000/datalake/silver/food_imports"
    df_silver.write.mode("overwrite").parquet(silver_path)

    print(f"✅ Datos guardados exitosamente en: {silver_path}")
    spark.stop()

if __name__ == "__main__":
    run_silver_transformation()