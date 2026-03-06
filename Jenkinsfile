pipeline {
    agent any
    
    environment {
        // Variables de entorno para facilitar lecturas
        SPARK_SUBMIT = "spark-submit"
    }

    stages {
        stage('🛠️ Setup & Install') {
            steps {
                echo 'Instalando dependencias de Python...'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('🥉 Ingesta (Bronze Layer)') {
            steps {
                echo 'Ejecutando ingesta de datos a HDFS...'
                sh '${SPARK_SUBMIT} src/ingestion/bronze_ingestion.py'
            }
        }
        stage('🥈 Transformación (Silver Layer)') {
            steps {
                echo 'Limpiando datos con PySpark...'
                sh '${SPARK_SUBMIT} src/processing/silver_transformation.py'
            }
        }
        stage('🥇 Enriquecimiento (Gold Layer)') {
            steps {
                echo 'Generando KPIs principales...'
                sh '${SPARK_SUBMIT} src/processing/poblar_capa_functional.py'
                echo 'Generando Agregaciones extra...'
                sh '${SPARK_SUBMIT} src/processing/gold_aggregation.py'
            }
        }
        stage('🍃 Exportar a MongoDB') {
            steps {
                echo 'Migrando a base de datos NoSQL...'
                sh '${SPARK_SUBMIT} --packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0 src/utils/export_gold_to_mongo.py'
            }
        }
        stage('📄 Exportar a CSV (BI)') {
            steps {
                echo 'Preparando archivo para Power BI...'
                sh '${SPARK_SUBMIT} src/utils/export_gold_to_csv.py'
            }
        }
    }
    post {
        success {
            echo '✅ Pipeline completado con éxito. ¡Los datos están listos en Mongo, Hive y CSV!'
        }
        failure {
            echo '❌ Ocurrió un error en el Pipeline. Revisa los logs de los stages.'
        }
    }
}