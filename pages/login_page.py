from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://www.saucedemo.com/"

    # Locators (Privados y centralizados)
    _USER_INPUT = (By.ID, "user-name")
    _PASS_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(self.URL)
        return self

    def completar_usuario(self, usuario: str):
        campo = self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        campo.clear()
        campo.send_keys(usuario)
        return self

    def completar_clave(self, clave: str):
        campo = self.driver.find_element(*self._PASS_INPUT)
        campo.clear()
        campo.send_keys(clave)
        return self

    def hacer_clic_login(self):
        self.driver.find_element(*self._LOGIN_BUTTON).click()

    def login_completo(self, usuario, clave):
        self.completar_usuario(usuario)
        self.completar_clave(clave)
        self.hacer_clic_login()
        return self

    def obtener_mensaje_error(self) -> str:
        try:
            elemento = self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            return elemento.text
        except:
            return ""