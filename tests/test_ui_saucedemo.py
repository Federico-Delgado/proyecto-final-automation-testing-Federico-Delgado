import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.datos import leer_csv_login, leer_json_productos
from utils.logger import logger # <--- NUEVO: Importar el logger

CSV_LOGIN = 'datos/usuarios_login.csv'
JSON_PRODUCTOS = 'datos/productos.json'

@pytest.mark.ui
@pytest.mark.e2e
def test_flujo_checkout_completo(driver):
    logger.info("=== INICIANDO: test_flujo_checkout_completo ===")
    
    login_page = LoginPage(driver)
    logger.info("Navegando a la página de login...")
    login_page.abrir()
    
    logger.info("Ingresando credenciales de standard_user...")
    login_page.login_completo("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(driver)
    logger.info("Agregando primer producto al carrito...")
    inventory_page.agregar_primer_producto()
    
    assert inventory_page.obtener_contador_carrito() == 1
    logger.info("Verificación exitosa: contador del carrito es 1")
    
    cart_page = inventory_page.ir_al_carrito()
    checkout_page = cart_page.proceder_checkout()
    
    logger.info("Completando información de checkout...")
    checkout_page.completar_informacion("Federico", "Delgado", "12345")
    checkout_page.continuar_checkout()
    checkout_page.finalizar_compra()
    
    assert checkout_page.es_compra_exitosa()
    assert "checkout-complete.html" in driver.current_url
    logger.info("=== FINALIZADO: test_flujo_checkout_completo (ÉXITO) ===")