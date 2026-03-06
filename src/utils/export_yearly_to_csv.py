from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, round

def export_yearly_country_data():
    # Iniciamos Spark con las buenas prácticas de compresión
    spark = SparkSession.builder \
        .appName("FoodImports_ExportYearlyCountry") \
        .config("spark.sql.parquet.compression.codec", "snappy") \
        .getOrCreate()

    print("\n" + "="*60)
    print("📈 ETL: Exportando Tendencias Anuales por País y Categoría")
    print("="*60)

    # 1. Leer datos de la Capa Curated (Silver) - AQUÍ ESTÁ EL DETALLE DEL PAÍS
    silver_path = "hdfs://localhost:9000/datalake/silver/food_imports"
    
    try:
        print(f"📥 Leyendo datos limpios desde HDFS: {silver_path}...")
        df_silver = spark.read.parquet(silver_path)
        
        # 2. Agrupación Analítica (On-the-fly): Año + País + Categoría
        # Sumamos los valores para obtener el total por esta combinación
        print("📊 Calculando agregaciones por Año, País y Categoría...")
        df_grouped = df_silver.groupBy("YearNum", "Country", "Category") \
            .agg(round(sum("FoodValue"), 2).alias("YearlyValue_MillionUSD"))
            
        # Ordenamos cronológicamente y alfabéticamente para Power BI
        df_final = df_grouped.orderBy("YearNum", "Country", "Category")
        
        # 3. Exportar a CSV consolidado en la carpeta processed
        # Usamos coalesce(1) para generar UN SOLO archivo CSV
        output_path = "file:/home/hadoop/topicos-food-imports/data/processed/yearly_export"
        
        print(f"📤 Exportando CSV consolidado a local: {output_path}...")
        df_final.coalesce(1) \
            .write \
            .mode("overwrite") \
            .option("header", "true") \
            .csv(output_path)
            
        print(f"✅ ¡Éxito! Archivo generado correctamente.")
        print("\n👀 Muestra del esquema exportado (YearNum, Country, Category, Value):")
        df_final.printSchema()
        print("👀 Muestra de los datos exportados (Top 5):")
        df_final.show(5)
        
    except Exception as e:
        print(f"❌ Error crítico en el ETL: {e}")
        print("💡 TIP: Asegúrate de que Hadoop esté corriendo y que 'silver_transformation.py' se haya ejecutado exitosamente.")
        
    print("="*60 + "\n")
    spark.stop()

if __name__ == "__main__":
    export_yearly_country_data()