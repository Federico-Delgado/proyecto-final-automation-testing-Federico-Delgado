from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Verificar que estamos en la página correcta
        self.wait.until(EC.url_contains("cart.html"))

    def obtener_nombres_productos(self):
        """Obtiene los nombres de todos los productos en el carrito de forma robusta."""
        # Esperar a que al menos un elemento esté presente
        self.wait.until(EC.presence_of_element_located(self._ITEM_NAMES))
        
        # Solución definitiva: Usar JavaScript para extraer todos los textos 
        # en una sola operación atómica. Esto evita por completo el 
        # StaleElementReferenceException en aplicaciones React.
        script = """
        var elements = document.querySelectorAll('.inventory_item_name');
        var texts = [];
        for (var i = 0; i < elements.length; i++) {
            texts.push(elements[i].innerText.trim());
        }
        return texts;
        """
        return self.driver.execute_script(script)

    def continuar_comprando(self):
        """Regresa a la página de inventario."""
        self.driver.find_element(*self._CONTINUE_SHOPPING).click()
        from pages.inventory_page import InventoryPage
        return InventoryPage(self.driver)

    def proceder_checkout(self):
        """Inicia el proceso de checkout."""
        self.driver.find_element(*self._CHECKOUT_BUTTON).click()
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)