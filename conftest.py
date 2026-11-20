import pytest
import os
import pathlib
from datetime import datetime
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def _is_ci_environment() -> bool:
    """
    Detecta si estamos ejecutando en un entorno de CI/CD (GitHub Actions, Jenkins, etc.).
    GitHub Actions setea automáticamente las variables CI=true y GITHUB_ACTIONS=true.
    """
    return os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"

@pytest.fixture(scope="function")
def driver():
    """
    Fixture que proporciona un WebDriver de Chrome configurado.
    - En local: abre Chrome con interfaz gráfica (visible).
    - En CI/CD: activa modo headless para que Chrome pueda ejecutarse sin pantalla.
    """
    chrome_options = Options()

    # Opciones comunes a ambos entornos
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Opciones específicas para CI/CD (Linux sin display)
    if _is_ci_environment():
        print("🚀 [CI] Ejecutando en modo headless (sin interfaz gráfica)")
        chrome_options.add_argument("--headless=new")  # Nuevo modo headless de Chrome
        chrome_options.add_argument("--disable-gpu")   # Evita errores de GPU en Linux
        chrome_options.add_argument("--remote-debugging-port=9222")

    service = Service()  # Selenium Manager gestiona el driver automáticamente
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.implicitly_wait(5)
    driver.maximize_window()

    yield driver

    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar screenshots automáticos en fallos y adjuntarlos al reporte."""
    outcome = yield
    report = outcome.get_result()
    
    # Solo capturamos si el test falló en la fase de ejecución principal ('call')
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            # Asegurar que la carpeta exista
            screens_dir = pathlib.Path('reports/screens')
            screens_dir.mkdir(parents=True, exist_ok=True)
            
            # Nombre descriptivo: FechaHora_NombreDelTest.png
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = screens_dir / f"{timestamp}_{item.name}.png"
            
            # Tomar la captura
            driver.save_screenshot(str(file_name))
            
            # Adjuntar al reporte HTML embebido en base64
            try:
                import pytest_html
                if not hasattr(report, 'extras'):
                    report.extras = []
                
                with open(file_name, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                
                report.extras.append(pytest_html.extras.image(image_data, mime_type='image/png'))
            except ImportError:
                pass 