from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, round, desc

def run_gold_aggregation():
    spark = SparkSession.builder \
        .appName("FoodImports_GoldAggregation") \
        .master("local[*]") \
        .getOrCreate()

    print("--- 🥇 Iniciando Agregaciones Avanzadas (Gold) ---")

    silver_path = "hdfs://localhost:9000/datalake/silver/food_imports"
    df_silver = spark.read.parquet(silver_path)

    # Nuevo KPI: Promedio de importación por Categoría
    df_avg_category = df_silver.groupBy("Category") \
        .agg(round(avg("FoodValue"), 2).alias("Promedio_Millones_USD")) \
        .orderBy(desc("Promedio_Millones_USD"))

    print("📊 KPI: Promedio de Valor por Categoría:")
    df_avg_category.show()

    # Guardar en HDFS
    gold_avg_path = "hdfs://localhost:9000/datalake/gold/food_imports_avg_category"
    df_avg_category.write.mode("overwrite").parquet(gold_avg_path)
    
    print(f"✅ Agregación guardada en {gold_avg_path}")
    spark.stop()

if __name__ == "__main__":
    run_gold_aggregation()