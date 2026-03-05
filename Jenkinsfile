pipeline {
    agent any
    stages {
        stage('🥇 Enriquecimiento (Gold)') {
            steps {
                echo 'Generando KPIs...'
                sh 'spark-submit src/processing/gold_aggregation.py'
            }
        }
        stage('🍃 Exportar a MongoDB') {
            steps {
                echo 'Migrando a NoSQL...'
                sh 'spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0 src/utils/export_gold_to_mongo.py'
            }
        }
    }
}