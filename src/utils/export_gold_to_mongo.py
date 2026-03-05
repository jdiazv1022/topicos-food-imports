from pyspark.sql import SparkSession

def export_to_mongo():
    # 🌟 1. Iniciar Spark con toda la energía
    print("🚀 [1/4] Inicializando Apache Spark Session...")
    spark = SparkSession.builder \
        .appName("FoodImports_ExportToMongo") \
        .master("local[*]") \
        .getOrCreate()

    print("✅ ¡Spark levantado con éxito!")
    print("--------------------------------------------------")
    print("🐘 Iniciando Exportación de HDFS a MongoDB 🍃")
    print("--------------------------------------------------")

    # 📂 2. Leer los datos de la Capa Functional (Gold) en HDFS
    print("📥 [2/4] Leyendo datos desde la Capa Gold en HDFS...")
    functional_path = "hdfs://localhost:9000/datalake/gold/food_imports_by_country"
    
    try:
        df_functional = spark.read.parquet(functional_path)
        print("✅ ¡Datos leídos correctamente!")
        
        print("📊 Vista previa de los datos a exportar (Top 5):")
        df_functional.show(5)
    except Exception as e:
        print(f"❌ Error al leer los datos de HDFS: {e}")
        spark.stop()
        return

    # 🍃 3. Escribir en MongoDB con opciones EXPLÍCITAS para el conector v10+
    print("📤 [3/4] Preparando conexión a MongoDB (usda_food.imports_by_country)...")
    
    # 💡 Nota: Como Mongo está en Windows y tú en WSL, 127.0.0.1 debería funcionar gracias al localhost forwarding de Windows 11.
    try:
        df_functional.write \
            .format("mongodb") \
            .option("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1:27017/") \
            .option("database", "usda_food") \
            .option("collection", "imports_by_country") \
            .mode("overwrite") \
            .save()
            
        print("✅ ¡Conexión y escritura completadas!")
    except Exception as e:
        print(f"❌ Error al escribir en MongoDB: {e}")
        print("💡 TIP: Verifica que no haya un firewall en Windows bloqueando el puerto 27017.")
        spark.stop()
        return

    # 🎉 4. Cierre exitoso
    print("--------------------------------------------------")
    print("🎉🏆 [4/4] ¡MIGRACIÓN A MONGODB COMPLETADA EXITOSAMENTE! 🏆🎉")
    print("--------------------------------------------------")
    
    spark.stop()
    print("🔌 Sesión de Spark cerrada.")

if __name__ == "__main__":
    export_to_mongo()