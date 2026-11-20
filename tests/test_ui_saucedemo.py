import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.datos import leer_csv_login, leer_json_productos

# Rutas a los archivos de datos
CSV_LOGIN = 'datos/usuarios_login.csv'
JSON_PRODUCTOS = 'datos/productos.json'

# --- TEST 1 y 2: Login Parametrizado (Incluye Escenario Negativo) ---
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.parametrize("usuario, clave, esperado_exitoso, descripcion", leer_csv_login(CSV_LOGIN))
def test_login_parametrizado(driver, usuario, clave, esperado_exitoso, descripcion):
    """Prueba login con múltiples usuarios (válidos, bloqueados, inválidos)."""
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.login_completo(usuario, clave)
    
    if esperado_exitoso:
        inventory_page = InventoryPage(driver)
        assert "inventory.html" in driver.current_url, "No redirigió al inventario"
        assert inventory_page.obtener_titulo() == "Products"
    else:
        error_msg = login_page.obtener_mensaje_error()
        assert error_msg != "", f"Se esperaba un mensaje de error para: {descripcion}"

# --- TEST 3: Agregar producto al carrito (Parametrizado con JSON) ---
@pytest.mark.ui
@pytest.mark.parametrize("nombre_producto, precio", leer_json_productos(JSON_PRODUCTOS))
def test_agregar_producto_al_carrito(driver, nombre_producto, precio):
    """Verifica que se puede agregar cada producto del JSON al carrito."""
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.login_completo("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(driver)
    inventory_page.agregar_producto_por_nombre(nombre_producto)
    
    assert inventory_page.obtener_contador_carrito() == 1
    
    cart_page = inventory_page.ir_al_carrito()
    productos_en_carrito = cart_page.obtener_nombres_productos()
    assert nombre_producto in productos_en_carrito

# --- TEST 4: Flujo Completo de Checkout (E2E) ---
@pytest.mark.ui
@pytest.mark.e2e
def test_flujo_checkout_completo(driver):
    """Flujo End-to-End: Login -> Agregar al carrito -> Checkout -> Compra exitosa."""
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.login_completo("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(driver)
    inventory_page.agregar_primer_producto()
    assert inventory_page.obtener_contador_carrito() == 1
    
    cart_page = inventory_page.ir_al_carrito()
    checkout_page = cart_page.proceder_checkout()
    
    checkout_page.completar_informacion("Federico", "Delgado", "12345")
    checkout_page.continuar_checkout()
    checkout_page.finalizar_compra()
    
    assert checkout_page.es_compra_exitosa()
    assert "checkout-complete.html" in driver.current_url

# --- TEST 5: Logout ---
@pytest.mark.ui
def test_logout(driver):
    """Verifica que el usuario puede cerrar sesión correctamente."""
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.login_completo("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(driver)
    login_page_final = inventory_page.hacer_logout()
    
    assert "saucedemo.com" in driver.current_url
    assert "inventory.html" not in driver.current_url