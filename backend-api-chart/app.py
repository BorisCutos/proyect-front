from flask import Flask, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL del backend-data
BACKEND_DATA_URL = "http://backend-data.k-att-y70-dev.svc.cluster.local:3000"

@app.route('/', methods=['GET'])
def get_users():
    """
    Endpoint principal que llama a backend-data
    """
    try:
        logger.info(f"Backend-API: Llamando a backend-data en {BACKEND_DATA_URL}/users")
        
        # Llamar a backend-data
        response = requests.get(f"{BACKEND_DATA_URL}/users", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Backend-API: Datos recibidos exitosamente de backend-data")
        
        return jsonify(data), 200
        
    except requests.exceptions.Timeout:
        logger.error("Backend-API: Timeout al conectar con backend-data")
        return jsonify({
            "error": "Timeout al conectar con backend-data",
            "service": "backend-api"
        }), 504
        
    except requests.exceptions.ConnectionError:
        logger.error("Backend-API: No se pudo conectar con backend-data")
        return jsonify({
            "error": "No se pudo conectar con backend-data",
            "service": "backend-api"
        }), 503
        
    except Exception as e:
        logger.error(f"Backend-API: Error inesperado: {str(e)}")
        return jsonify({
            "error": str(e),
            "service": "backend-api"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint de health check
    """
    return jsonify({
        "status": "healthy",
        "service": "backend-api"
    }), 200

if __name__ == '__main__':
    logger.info("Backend-API iniciando en puerto 3000...")
    app.run(host='0.0.0.0', port=3000, debug=False)