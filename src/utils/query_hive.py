from pyspark.sql import SparkSession

def query_hive():
    # Iniciamos Spark conectado a Hive
    spark = SparkSession.builder \
        .appName("Query_Hive_Tables") \
        .enableHiveSupport() \
        .getOrCreate()

    print("\n" + "="*50)
    print("🐝 CONSULTA ANALÍTICA EN APACHE HIVE (TOP 5)")
    print("="*50)
    
    # Seleccionamos tu base de datos
    spark.sql("USE usda_food")
    
    # Ejecutamos SQL avanzado: Ordenado, filtrando "WORLD" y formateando decimales
    top_5 = spark.sql("""
        SELECT 
            Country as Pais_Origen, 
            CAST(TotalValue_MillionUSD AS DECIMAL(15,2)) as Millones_USD
        FROM imports_by_country 
        WHERE Country NOT LIKE '%WORLD%' 
        ORDER BY TotalValue_MillionUSD DESC 
        LIMIT 5
    """)
    
    # .show() es lo que dibuja la tabla perfecta en la consola
    top_5.show()
    
    print("="*50 + "\n")
    spark.stop()

if __name__ == "__main__":
    query_hive()