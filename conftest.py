import pytest
import pathlib
from datetime import datetime
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    """Fixture que proporciona un WebDriver de Chrome configurado."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Descomentar para CI/CD (Fase 5)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service()
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