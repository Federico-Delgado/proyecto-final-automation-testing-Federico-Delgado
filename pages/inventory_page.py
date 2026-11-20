from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    _TITLE = (By.CLASS_NAME, "title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def obtener_titulo(self):
        return self.driver.find_element(*self._TITLE).text

    def obtener_productos(self):
        return self.driver.find_elements(*self._PRODUCTS)

    def agregar_primer_producto(self):
        primer_boton = self.driver.find_elements(*self._ADD_BUTTONS)[0]
        primer_boton.click()
        return self

    def agregar_producto_por_nombre(self, nombre_producto: str):
        """Añade un producto específico al carrito usando su nombre."""
        xpath = f"//div[text()='{nombre_producto}']/ancestor::div[@class='inventory_item']//button"
        boton = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        boton.click()
        return self

    def obtener_contador_carrito(self):
        try:
            badge = self.driver.find_element(*self._CART_BADGE)
            return int(badge.text)
        except:
            return 0

    def ir_al_carrito(self):
        self.driver.find_element(*self._CART_LINK).click()
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def hacer_logout(self):
        """Cierra la sesión del usuario y espera a que la página de login cargue completamente."""
        # 1. Abrir el menú lateral de forma segura (Corregido el NameError)
        menu_btn = self.wait.until(EC.element_to_be_clickable(self._MENU_BUTTON))
        menu_btn.click()
        
        # 2. Hacer clic en el enlace de logout
        logout_link = self.wait.until(EC.element_to_be_clickable(self._LOGOUT_LINK))
        logout_link.click()
        
        # 3. Esperar explícitamente a que la página de login se cargue
        from pages.login_page import LoginPage
        login_page = LoginPage(self.driver)
        self.wait.until(EC.visibility_of_element_located(login_page._LOGIN_BUTTON))
        
        return login_page