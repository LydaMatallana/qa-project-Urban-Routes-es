import time
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    # Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    button_order_taxi = (
    By.XPATH, '//div[@class="type-picker shown"]/div[@class="results-container"]/div[@class="results-text"]/button')
    comfort_fare = (By.XPATH, '//div[@class="tariff-cards"]/div[5]')
    title_fare = (By.XPATH, "//div[contains(text(),'Comfort')]/..//div[@class='tcard-title']")
    phone_number_field = (By.CLASS_NAME, 'np-text')
    first_phone_number = (By.CSS_SELECTOR, '.active .label')
    input_phone_number = (By.ID, 'phone')
    next_button = (By.XPATH, "//div[@class='section active']//form//div[@class='buttons']//button[@type='submit']")
    input_code = (By.ID, "code")
    confirm_button = (By.XPATH, "//*[@id='root']/div/div[1]/div[2]/div[1]/button") #Solo se logró ubicar de esta forma
    payment_method = (By.CLASS_NAME, 'pp-text')
    credit_card_option = (By.CLASS_NAME, "pp-plus")
    input_credit_card_number = (By.ID, "number")
    input_card_code = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    focusing_code_card = (By.CSS_SELECTOR, ".plc")
    confirm_credit_card = (By.XPATH, "//div[@class='pp-buttons']//button[@type='submit']")
    close_credit_card_option = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button") #Solo se logró ubicar de esta forma
    message_driver_field = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[3]/div/label") #Solo se logró ubicar de esta forma
    message_for_driver = (By.ID, "comment")
    blanket_tissues_option = (
    By.XPATH, "//div[@class='r-sw-container']/*[contains(text(),'Manta')]/..//div[@class='switch']")
    ice_cream_option = (By.XPATH, "//div[contains(text(),'Helado')]/..//div[@class='counter-plus']")
    ice_cream_quantity =(By.XPATH, "//div[contains(text(),'Helado')]/..//div[@class='counter-value']")
    button_search_taxi = (By.CSS_SELECTOR, ".smart-button-secondary")
    title_modal = (By.CLASS_NAME, "order-header-title")

    # Métodos
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address): #Método para ingresar dirección desde
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address): #Método para ingresar dirección hasta
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self): #Método para obtener dirección desde
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self): #Método para obtener dirección hasta
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_button_order_taxi(self):  #Método para hacer click sobre el botón pedir taxi
        return self.driver.find_element(*self.button_order_taxi).click()

    def click_comfort_fare(self):  #Método para seleccionar la tarifa confort
        return self.driver.find_element(*self.comfort_fare).click()

    def click_phone_number(self):  #Método para dar click sobre el campo nro de teléfono
        return self.driver.find_element(*self.phone_number_field).click()

    def click_input_phone(self):  #Método para dar click sobre el campo introducir nro de teléfono
        return self.driver.find_element(*self.first_phone_number).click()

    def fill_phone_number(self):  #Método para ingresar el número de teléfono
        return self.driver.find_element(*self.input_phone_number).send_keys(data.phone_number)

    def get_phone_number(self): #Método para obtener el número de teléfono
        return self.driver.find_element(*self.input_phone_number).get_property('value')

    def click_next(self):  #Método para dar click sobre el botón siguiente
        return self.driver.find_element(*self.next_button).click()

    def click_code(self):  #Método para dar click sobre el campo código
        return self.driver.find_element(*self.input_code).click()

    def get_code(self):  #Método para ingresar el código
        return self.driver.find_element(*self.input_code).send_keys(retrieve_phone_code(self.driver))

    def click_input_payment_method(self):  #Método para dar click sobre el metodo de pago
        return self.driver.find_element(*self.payment_method).click()

    def click_select_credit_card(self):  #Método para agregar TC
        return self.driver.find_element(*self.credit_card_option).click()

    def fill_credit_card(self):  #Método para ingresar nro de TC
        return self.driver.find_element(*self.input_credit_card_number).send_keys(data.card_number)

    def get_credit_card(self):  # Método para que tome el valor de la tarjeta
        return self.driver.find_element(*self.input_credit_card_number).get_property('value')

    def fill_code_credit_card(self):  #Método para dar click en el campo código
        return self.driver.find_element(*self.input_card_code).click()

    def click_code_credit_card(self):  #Método para ingresar código tarjeta de crédito
        return self.driver.find_element(*self.input_card_code).send_keys(data.card_code)

    def get_code_credit_card(self):  #Método para que tome el código tarjeta de crédito
        return self.driver.find_element(*self.input_card_code).get_property('value')

    def activate_add_button(self):  #Método para dar click fuera del campo codigo y que se active el botón agregar
        return self.driver.find_element(*self.focusing_code_card).click()

    def add_credit_card(self):  #Método para dar click en el botón agregar de la TC
        return self.driver.find_element(*self.confirm_credit_card).click()

    def close_credit_card(self):  #Método para cerrar ventana de la TC
        return self.driver.find_element(*self.close_credit_card_option).click()

    def click_message_driver(self):  #Método para dar click sobre el campo del mensaje al conductor
        return self.driver.find_element(*self.message_driver_field).click()

    def fill_message_driver(self):  #Método para ingresar mensaje para el conductor
        return self.driver.find_element(*self.message_for_driver).send_keys(data.message_for_driver)

    def get_message_driver(self): #Método para obtener mensaje para el conductor
        return self.driver.find_element(*self.message_for_driver).get_property('value')

    def select_blanket_tissues(self):  #Método para seleccionar opción de manta y pañuelos
        return self.driver.find_element(*self.blanket_tissues_option).click()

    def select_ice_cream(self):  #Método para seleccionar 2 helados (1er click)
        return self.driver.find_element(*self.ice_cream_option).click()

    def select_ice_cream(self):  #Método para seleccionar 2 helados (2do click para que queden seleccinados dos)
        return self.driver.find_element(*self.ice_cream_option).click()

    def select_search_taxi(self):  #Método para que aparezca el modal para buscar taxi
        return self.driver.find_element(*self.button_search_taxi).click()


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        capabilities = Options()
        capabilities.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=capabilities)
        cls.driver.implicitly_wait(10)

# Pruebas Urban Routes
    def test_set_route(self):
        # Ejercicio No. 1 Prueba Configurar la dirección
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_fare(self):
        # Ejercicio No. 2 Prueba seleccionar la tarifa Comfort
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_button_order_taxi()
        assert self.driver.find_element(*routes_page.title_fare).text == "Comfort"

    def test_fill_phone_number(self):
        # Ejercicio No. 3 Prueba rellenar el número de teléfono
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_button_order_taxi()
        routes_page.click_comfort_fare()
        routes_page.click_phone_number()
        routes_page.click_input_phone()
        routes_page.fill_phone_number()
        routes_page.get_phone_number()
        assert self.driver.find_element(*routes_page.input_phone_number).get_property('value') == data.phone_number

    def test_add_credit_card(self):
        # Ejercicio No. 4 Agregar una Tarjeta de Crédito
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_button_order_taxi()
        routes_page.click_comfort_fare()
        routes_page.click_input_payment_method()
        routes_page.click_select_credit_card()
        routes_page.fill_credit_card()
        routes_page.get_credit_card()
        routes_page.click_code_credit_card()
        routes_page.fill_code_credit_card()
        routes_page.get_code_credit_card()
        routes_page.activate_add_button()
        assert routes_page.get_credit_card() == data.card_number
        assert routes_page.get_code_credit_card() == data.card_code

    def test_mesagge_for_driver(self):
        # Ejercicio No. 5 Escribir un mensaje para el Conductor
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_button_order_taxi()
        routes_page.click_comfort_fare()
        routes_page.click_input_payment_method()
        routes_page.click_select_credit_card()
        routes_page.fill_credit_card()
        routes_page.get_credit_card()
        routes_page.click_code_credit_card()
        routes_page.fill_code_credit_card()
        routes_page.get_code_credit_card()
        routes_page.activate_add_button()
        routes_page.add_credit_card()
        routes_page.close_credit_card()
        routes_page.click_message_driver()
        routes_page.fill_message_driver()
        routes_page.get_message_driver()
        assert self.driver.find_element(*routes_page.message_for_driver).get_property(
            'value') == data.message_for_driver

    def test_select_blanket_and_tissues(self):
        # Ejercicio No. 6 Pedir una manta y pañuelos
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_button_order_taxi()
        routes_page.click_comfort_fare()
        routes_page.click_input_payment_method()
        routes_page.click_select_credit_card()
        routes_page.fill_credit_card()
        routes_page.get_credit_card()
        routes_page.click_code_credit_card()
        routes_page.fill_code_credit_card()
        routes_page.get_code_credit_card()
        routes_page.activate_add_button()
        routes_page.add_credit_card()
        routes_page.close_credit_card()
        routes_page.click_message_driver()
        routes_page.fill_message_driver()
        routes_page.get_message_driver()
        routes_page.select_blanket_tissues()
        assert self.driver.find_element(*routes_page.blanket_tissues_option).is_selected() == True

    def test_select_two_ice_cream(self):
        # Ejercicio No. 7 Pedir dos helados
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_button_order_taxi()
        routes_page.click_comfort_fare()
        routes_page.click_input_payment_method()
        routes_page.click_select_credit_card()
        routes_page.fill_credit_card()
        routes_page.get_credit_card()
        routes_page.click_code_credit_card()
        routes_page.fill_code_credit_card()
        routes_page.get_code_credit_card()
        routes_page.activate_add_button()
        routes_page.add_credit_card()
        routes_page.close_credit_card()
        routes_page.click_message_driver()
        routes_page.fill_message_driver()
        routes_page.get_message_driver()
        routes_page.select_blanket_tissues()
        routes_page.select_ice_cream()
        routes_page.select_ice_cream()
        assert self.driver.find_element(*routes_page.ice_cream_quantity).text == '2'
    def test_select_modal_taxi(self):
        # Ejercicio No. 8 Aparece el modal para buscar taxi
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_button_order_taxi()
        routes_page.click_comfort_fare()
        routes_page.click_input_payment_method()
        routes_page.click_select_credit_card()
        routes_page.fill_credit_card()
        routes_page.get_credit_card()
        routes_page.click_code_credit_card()
        routes_page.fill_code_credit_card()
        routes_page.get_code_credit_card()
        routes_page.activate_add_button()
        routes_page.add_credit_card()
        routes_page.close_credit_card()
        routes_page.click_message_driver()
        routes_page.fill_message_driver()
        routes_page.get_message_driver()
        routes_page.select_blanket_tissues()
        routes_page.select_ice_cream()
        routes_page.select_ice_cream()
        routes_page.select_search_taxi()
        assert self.driver.find_element(*routes_page.title_modal).text == "Buscar automóvil"


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
