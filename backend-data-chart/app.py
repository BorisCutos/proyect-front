from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import time
import os

app = Flask(__name__)
CORS(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la base de datos desde variables de entorno
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgresql.k-att-y70-dev.svc.cluster.local'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'proj-openshift'),
    'user': os.getenv('DB_USER', 'openshift'),
    'password': os.getenv('DB_PASSWORD', 'openshift')
}

def get_db_connection():
    """
    Crear conexión a PostgreSQL
    """
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error(f"Error conectando a la base de datos: {str(e)}")
        raise

def init_database():
    """
    Inicializar la base de datos: crear tabla y datos de ejemplo
    """
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Intento {attempt + 1} de conectar a la base de datos...")
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Crear tabla si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Verificar si ya hay datos
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()['count']
            
            # Insertar datos de ejemplo si la tabla está vacía
            if count == 0:
                logger.info("Insertando datos de ejemplo...")
                sample_data = [
                    ('Juan Pérez', 'juan.perez@example.com'),
                    ('María García', 'maria.garcia@example.com'),
                    ('Carlos López', 'carlos.lopez@example.com'),
                    ('Ana Martínez', 'ana.martinez@example.com'),
                    ('Pedro Rodríguez', 'pedro.rodriguez@example.com')
                ]
                
                for name, email in sample_data:
                    cursor.execute(
                        "INSERT INTO users (name, email) VALUES (%s, %s)",
                        (name, email)
                    )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info("Base de datos inicializada correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en intento {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                logger.error("No se pudo inicializar la base de datos después de varios intentos")
                return False

@app.route('/users', methods=['GET'])
def get_users():
    """
    Obtener todos los usuarios de la base de datos
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY id")
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        logger.info(f"Backend-Data: Retornando {len(users)} usuarios")
        
        return jsonify({
            "users": users,
            "count": len(users),
            "service": "backend-data"
        }), 200
        
    except Exception as e:
        logger.error(f"Backend-Data: Error al consultar usuarios: {str(e)}")
        return jsonify({
            "error": str(e),
            "service": "backend-data"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint de health check con verificación de conexión a BD
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "service": "backend-data"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "service": "backend-data"
        }), 503

if __name__ == '__main__':
    logger.info("Backend-Data iniciando...")
    logger.info(f"Conectando a PostgreSQL en {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    
    # Inicializar base de datos
    if init_database():
        logger.info("Backend-Data iniciando en puerto 3000...")
        app.run(host='0.0.0.0', port=3000, debug=False)
    else:
        logger.error("No se pudo inicializar la base de datos. Saliendo...")
        exit(1)