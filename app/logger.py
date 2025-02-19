import logging
import os

# Crear directorio para logs si no existe
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configurar logger
log_file = os.path.join(LOG_DIR, "app.log")
logging.basicConfig(
    level=logging.DEBUG,  # Nivel de logging
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # Guardar en archivo
        logging.StreamHandler()  # Mostrar en consola
    ]
)

# Crear instancia de logger
logger = logging.getLogger("task-manager")
