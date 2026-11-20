from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _ZIP_CODE = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")
    _FINISH_BUTTON = (By.ID, "finish")
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def completar_informacion(self, nombre, apellido, codigo_postal):
        self.driver.find_element(*self._FIRST_NAME).send_keys(nombre)
        self.driver.find_element(*self._LAST_NAME).send_keys(apellido)
        self.driver.find_element(*self._ZIP_CODE).send_keys(codigo_postal)
        return self

    def continuar_checkout(self):
        self.driver.find_element(*self._CONTINUE_BUTTON).click()
        return self

    def finalizar_compra(self):
        self.driver.find_element(*self._FINISH_BUTTON).click()
        return self

    def es_compra_exitosa(self):
        try:
            header = self.wait.until(EC.visibility_of_element_located(self._COMPLETE_HEADER))
            return "THANK YOU" in header.text.upper() or "COMPLETE" in header.text.upper()
        except:
            return False