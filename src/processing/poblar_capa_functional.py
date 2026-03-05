from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, round, desc

def run_functional_layer():
    # 1. Iniciar sesión de Spark con buenas prácticas
    spark = SparkSession.builder \
        .appName("FoodImports_FunctionalLayer") \
        .master("local[*]") \
        .config("spark.sql.parquet.compression.codec", "snappy") \
        .getOrCreate()

    print("--- Iniciando Procesamiento Capa Functional (Analytics) ---")

    # 2. Leer datos de la capa Curated (Silver)
    curated_path = "hdfs://localhost:9000/datalake/silver/food_imports"
    df_curated = spark.read.parquet(curated_path)

    # 3. Transformaciones de Negocio (KPIs)
    # KPI 1: Valor total de importaciones por País (Top Histórico)
    df_kpi_country = df_curated.groupBy("Country") \
        .agg(round(sum("FoodValue"), 2).alias("TotalValue_MillionUSD")) \
        .orderBy(desc("TotalValue_MillionUSD"))

    # KPI 2: Valor de importaciones por Categoría y Año
    df_kpi_category_year = df_curated.groupBy("YearNum", "Category") \
        .agg(round(sum("FoodValue"), 2).alias("YearlyValue_MillionUSD")) \
        .orderBy("YearNum", desc("YearlyValue_MillionUSD"))

    # 4. Mostrar resultados en consola para validar
    print("Top 5 Países Proveedores:")
    df_kpi_country.show(5)

    # 5. Guardar en Capa Functional (Gold)
    functional_country_path = "hdfs://localhost:9000/datalake/gold/food_imports_by_country"
    functional_category_path = "hdfs://localhost:9000/datalake/gold/food_imports_by_category"
    
    df_kpi_country.write.mode("overwrite").parquet(functional_country_path)
    df_kpi_category_year.write.mode("overwrite").parquet(functional_category_path)

    print(f"--- Datos funcionales guardados exitosamente en {functional_country_path} ---")
    spark.stop()

if __name__ == "__main__":
    run_functional_layer()