"""
Script to create Hive tables using PySpark instead of Hive CLI.
This removes the dependency on the Hive command-line tool.
"""

from pyspark.sql import SparkSession
import os

def create_hive_tables():
    # Initialize Spark with Hive support enabled
    spark = SparkSession.builder \
        .appName("Create_Hive_Tables") \
        .enableHiveSupport() \
        .getOrCreate()

    print("\n" + "="*60)
    print("🐝 CREATING HIVE TABLES")
    print("="*60 + "\n")

    try:
        # Read the HQL file
        hql_file_path = "sql/hive/create_tables.hql"
        
        if not os.path.exists(hql_file_path):
            print(f"❌ Error: File not found: {hql_file_path}")
            return False
        
        with open(hql_file_path, 'r') as f:
            hql_content = f.read()
        
        # Remove comments (lines starting with --)
        lines = []
        for line in hql_content.split('\n'):
            # Remove comment part from the line
            if '--' in line:
                line = line[:line.index('--')]
            lines.append(line)
        
        # Rejoin and split by semicolon
        cleaned_content = '\n'.join(lines)
        statements = [
            stmt.strip() 
            for stmt in cleaned_content.split(';') 
            if stmt.strip()
        ]
        
        # Execute each statement
        for i, statement in enumerate(statements, 1):
            print(f"📝 Executing statement {i}...")
            preview = statement.replace('\n', ' ').strip()
            print(f"   {preview[:80]}..." if len(preview) > 80 else f"   {preview}")
            
            try:
                spark.sql(statement)
                print(f"   ✅ Success\n")
            except Exception as e:
                print(f"   ⚠️  Warning/Error: {str(e)}\n")
        
        print("="*60)
        print("✅ HIVE TABLE CREATION COMPLETED")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return False
    
    finally:
        spark.stop()

if __name__ == "__main__":
    success = create_hive_tables()
    exit(0 if success else 1)
