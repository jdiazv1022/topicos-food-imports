import yaml
import os

def get_mongo_config():
    """
    Lee el archivo settings.yaml y devuelve la configuración de MongoDB.
    """
    config_path = os.path.join(os.getcwd(), 'config', 'settings.yaml')
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        mongo_uri = config['mongodb']['uri']
        mongo_db = config['mongodb']['database']
        mongo_coll = config['mongodb']['collection']
        
        return mongo_uri, mongo_db, mongo_coll
    except Exception as e:
        print(f"❌ Error leyendo settings.yaml: {e}")
        return None, None, None

# Test rápido
if __name__ == "__main__":
    uri, db, coll = get_mongo_config()
    print(f"✅ Configuración cargada: URI={uri}, DB={db}, Colección={coll}")