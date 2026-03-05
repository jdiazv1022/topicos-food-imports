from pyspark.sql import SparkSession

def export_to_csv():
    # 1. Iniciar Spark
    spark = SparkSession.builder \
        .appName("FoodImports_ExportToCSV") \
        .getOrCreate()

    print("--- 📄 Exportando Capa Gold a CSV para Power BI ---")

    # 2. Leer los datos de la Capa Functional (Gold)
    gold_path = "hdfs://localhost:9000/datalake/gold/food_imports_by_country"
    df_gold = spark.read.parquet(gold_path)

    # 3. Guardar como CSV en tu carpeta local
    # Usamos coalesce(1) para que genere un solo archivo CSV y no varios pedacitos
    output_path = "file:/home/hadoop/topicos-food-imports/data/processed/gold_export"
    
    df_gold.coalesce(1) \
        .write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(output_path)

    print(f"✅ Exportación completada exitosamente en: {output_path}")
    spark.stop()

if __name__ == "__main__":
    export_to_csv()