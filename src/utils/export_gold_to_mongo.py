from pyspark.sql import SparkSession

def export_to_mongo():
    print("🚀 [1/4] Inicializando Apache Spark Session...")
    spark = SparkSession.builder \
        .appName("FoodImports_ExportToMongo") \
        .master("local[*]") \
        .getOrCreate()

    print("✅ ¡Spark levantado con éxito!")
    print("-" * 50)
    print("🐘 Iniciando Exportación de HDFS a MongoDB 🍃")
    print("-" * 50)

    print("📥 [2/4] Leyendo datos desde la Capa Gold en HDFS...")
    functional_path = "hdfs://localhost:9000/datalake/gold/food_imports_by_country"
    
    try:
        df_functional = spark.read.parquet(functional_path)
        print("✅ ¡Datos leídos correctamente!")
        print("📊 Vista previa de los datos a exportar (Top 5):")
        df_functional.show(5, truncate=False)
    except Exception as e:
        print(f"❌ Error al leer los datos de HDFS: {e}")
        spark.stop()
        return

    print("📤 [3/4] Preparando conexión a MongoDB (usda_food.imports_by_country)...")
    
    try:
        from pymongo import MongoClient
        
        # Convertir datos de Spark a Python/Pandas
        data_list = df_functional.toJSON().map(lambda x: __import__('json').loads(x)).collect()
        
        # Conectar a MongoDB
        client = MongoClient('mongodb://127.0.0.1:27017/')
        db = client['usda_food']
        collection = db['imports_by_country']
        
        # Limpiar colección anterior
        collection.delete_many({})
        
        # Insertar nuevos datos
        if data_list:
            collection.insert_many(data_list)
            print(f"✅ ¡{len(data_list)} documentos insertados en MongoDB!")
        else:
            print("⚠️ No hay datos para insertar")
            
        client.close()
    except Exception as e:
        print(f"❌ Error al escribir en MongoDB: {e}")
        spark.stop()
        return

    print("-" * 50)
    print("🎉🏆 [4/4] ¡MIGRACIÓN A MONGODB COMPLETADA EXITOSAMENTE! 🏆🎉")
    print("-" * 50)
    
    spark.stop()

if __name__ == "__main__":
    export_to_mongo()