import subprocess
import time

def run_step(step_name, command):
    print(f"\n{'='*70}")
    print(f"🚀 INICIANDO: {step_name}")
    print(f"{'='*70}")
    
    start_time = time.time()
    
    try:
        # Ejecuta el comando de Spark en la terminal
        subprocess.run(command, shell=True, check=True)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        print(f"\n✅ ÉXITO: '{step_name}' completado en {duration} segundos.\n")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR CRÍTICO en {step_name}.")
        print("⚠️ Deteniendo el pipeline completo para evitar corrupción de datos.")
        exit(1) # Detiene el script si hay un error

def run_full_pipeline():
    print("🌟 BIENVENIDO AL ORQUESTADOR DEL PIPELINE - FOOD IMPORTS 🌟")
    print("Iniciando Arquitectura Medallón automatizada...\n")

    total_start = time.time()

    # 1. Capa Silver (Limpieza y Calidad de Datos)
    run_step(
        "1. CAPA SILVER (Limpieza y Filtros)", 
        "spark-submit src/processing/silver_transformation.py"
    )

    # 2. Capa Gold (Cálculo de KPIs principales)
    run_step(
        "2. CAPA GOLD (Cálculo de KPIs)", 
        "spark-submit src/processing/poblar_capa_functional.py"
    )

    # 3. Exportación a CSV para Power BI (Datos Agrupados)
    run_step(
        "3. EXPORTACIÓN CSV (Top Países)", 
        "spark-submit src/utils/export_gold_to_csv.py"
    )

    # 4. Exportación a CSV para Power BI (Tendencias en el tiempo)
    run_step(
        "4. EXPORTACIÓN CSV (Tendencias Anuales)", 
        "spark-submit src/utils/export_yearly_to_csv.py"
    )

    # 5. Exportación a MongoDB
    run_step(
        "5. EXPORTACIÓN A MONGODB", 
        "spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0 src/utils/export_gold_to_mongo.py"
    )

    total_end = time.time()
    total_duration = round((total_end - total_start) / 60, 2)

    print(f"{'='*70}")
    print(f"🎉🏆 PIPELINE COMPLETADO AL 100% EN {total_duration} MINUTOS 🏆🎉")
    print("Todos los datos están listos en HDFS, Power BI y MongoDB.")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    run_full_pipeline()