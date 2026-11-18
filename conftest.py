import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture(scope="function")
def driver():
    """Fixture que proporciona un WebDriver de Chrome configurado."""
    chrome_options = Options()
    # Descomentar la siguiente línea para ejecutar en modo headless (ideal para CI/CD en Fase 5)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service() # Selenium 4 gestiona el driver automáticamente
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.implicitly_wait(5) # Espera implícita de seguridad
    driver.maximize_window()
    
    yield driver
    
    # Teardown: cerrar el navegador después de cada test
    driver.quit()