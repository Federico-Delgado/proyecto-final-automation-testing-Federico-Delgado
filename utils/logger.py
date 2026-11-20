import logging
import pathlib
from logging.handlers import RotatingFileHandler

# 1. Crear carpeta 'logs' si no existe
log_dir = pathlib.Path('logs')
log_dir.mkdir(exist_ok=True)

# 2. Configurar el logger principal
logger = logging.getLogger('automation_framework')
logger.setLevel(logging.INFO)

# 3. Evitar duplicar handlers si el módulo se importa múltiples veces
if not logger.handlers:
    # Handler para archivo (Rota cada 5MB, mantiene 3 archivos de respaldo)
    file_handler = RotatingFileHandler(
        log_dir / 'suite.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    # Handler para consola (Solo muestra WARNING y ERROR para no ensuciar la salida de pytest)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # 4. Formato profesional: Fecha | Nivel | Nombre del Logger | Mensaje
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)