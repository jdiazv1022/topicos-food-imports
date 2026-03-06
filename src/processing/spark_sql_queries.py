from pyspark.sql import SparkSession

def run_spark_sql_queries():
    print("🐝 Iniciando Spark SQL para consultas tipo Hive...")
    
    spark = SparkSession.builder \
        .appName("FoodImports_HiveQueries") \
        .master("local[*]") \
        .enableHiveSupport() \
        .getOrCreate()

    print("✅ ¡Spark con soporte Hive levantado!")
    print("-" * 60)
    
    # Crear base de datos
    print("🔨 Creando base de datos usda_food...")
    spark.sql("CREATE DATABASE IF NOT EXISTS usda_food")
    print("✅ ¡Base de datos creada!")
    
    # Crear tabla externa
    print("\n📊 Creando tabla externa imports_by_country...")
    spark.sql("""
        CREATE EXTERNAL TABLE IF NOT EXISTS usda_food.imports_by_country (
            Country STRING,
            TotalValue_MillionUSD DOUBLE
        )
        STORED AS PARQUET
        LOCATION 'hdfs://localhost:9000/datalake/gold/food_imports_by_country'
    """)
    print("✅ ¡Tabla creada!")
    
    # Ejecutar consulta
    print("\n🔍 Ejecutando consulta SQL: Top 5 países por valor de importación")
    print("-" * 60)
    result = spark.sql("""
        SELECT * FROM usda_food.imports_by_country 
        ORDER BY TotalValue_MillionUSD DESC LIMIT 5
    """)
    
    print("✅ Resultados de la consulta SQL:")
    print("-" * 60)
    result.show(5, truncate=False)
    
    # Estadísticas adicionales
    print("\n📈 Estadísticas generales:")
    stats = spark.sql("""
        SELECT 
            COUNT(*) as total_countries,
            SUM(TotalValue_MillionUSD) as total_imports_million_usd,
            AVG(TotalValue_MillionUSD) as avg_imports_million_usd,
            MAX(TotalValue_MillionUSD) as max_imports_million_usd,
            MIN(TotalValue_MillionUSD) as min_imports_million_usd
        FROM usda_food.imports_by_country
    """)
    stats.show(truncate=False)
    
    print("\n" + "=" * 60)
    print("🎉 ¡CONSULTAS HIVE/SPARK SQL EJECUTADAS EXITOSAMENTE! 🎉")
    print("=" * 60)
    
    spark.stop()

if __name__ == "__main__":
    run_spark_sql_queries()
