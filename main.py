import time
from asyncio import timeout

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from data import phone_number, card_number, card_code


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
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.XPATH, '//button[text()="Pedir un taxi"]')
    comfort_button = (By.CLASS_NAME, 'tcard-title')
    phone_button = (By.CLASS_NAME, 'np-text')
    phone_field = (By.ID, 'phone')
    phone_button_next = (By.CLASS_NAME, 'button.full')
    code_field = (By.ID, 'code')
    code_confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    add_payment_button = (By.CLASS_NAME, 'pp-button.filled')
    add_card_button = (By.CLASS_NAME, 'pp-plus-container')
    card_field = (By.ID, 'number')
    cvv_field = (By.CSS_SELECTOR, 'input[placeholder="12"]')
    add_card_confirmation_button = (By.XPATH, '//button[text()="Agregar"]')
    card_section_button_close = (By.CSS_SELECTOR, 'div.payment-picker.open button.close-button.section-close')
    add_comment = (By.ID, 'comment')
    switch_blanket = (By.CSS_SELECTOR, ".slider.round")
    ice_cream_counter = (By.CSS_SELECTOR, '.counter-plus')
    counter_value = (By.CSS_SELECTOR, '.counter-value')
    service_confirmation_button = (By.CSS_SELECTOR, '.smart-button-secondary')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver,10).until(expected_conditions.presence_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)


    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_address)


    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def click_taxi_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.taxi_button))
        self.driver.find_element(*self.taxi_button).click()

    def click_comfort_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.comfort_button))
        buttons = self.driver.find_elements(*self.comfort_button)
        for button in buttons:
            if button.text == 'Comfort':
                button.click()
                break


    def click_phone_interaction(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.phone_button))
        self.driver.find_element(*self.phone_button).click()

    def filling_phone_field(self, number_phone):
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(self.phone_field))
        self.driver.find_element(*self.phone_field).send_keys(number_phone)

    def get_phone(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def click_next_button_after_phone_filling(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.phone_button_next))
        self.driver.find_element(*self.phone_button_next).click()

    def filling_phone_confirmation_code(self, code):
        time.sleep(1)
        #WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.code_field))
        self.driver.find_element(*self.code_field).send_keys(code)

    def click_confirm_button_after_code_filling(self):
        self.driver.find_element(*self.code_confirm_button).click()

    def click_add_payment_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.add_payment_button))
        self.driver.find_element(*self.add_payment_button).click()

    def click_add_card_button(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.add_card_button))
        self.driver.find_element(*self.add_card_button).click()

    def filling_card_field(self, card_data):
        self.driver.find_element(*self.card_field).send_keys(card_data)
        self.driver.find_element(*self.card_field).send_keys(Keys.TAB)

    def get_card_number(self):
        return self.driver.find_element(*self.card_field).get_property('value')

    def filling_cvv_field(self, cvv_code):
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located(self.cvv_field))
        cvv_input = self.driver.find_element(*self.cvv_field)
        cvv_input.send_keys(cvv_code)
        cvv_input.send_keys(Keys.TAB)

    def get_cvv_number(self):
        return self.driver.find_element(*self.cvv_field).get_property('value')

    def click_add_card_confirmation_button(self):
        WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable(self.add_card_confirmation_button))
        self.driver.find_element(*self.add_card_confirmation_button).click()

    def click_close_card_add_interaction(self, index):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.card_section_button_close))
        self.driver.find_element(*self.card_section_button_close).click()


    def add_comment_to_driver(self, comment):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.add_comment))
        self.driver.find_element(*self.add_comment).send_keys(comment)

    def get_comment_to_driver(self):
        return self.driver.find_element(*self.add_comment).get_property('value')

    def click_switch_blanket(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.switch_blanket))
        self.driver.find_element(*self.switch_blanket).click()

    def add_ice_cream(self):
        WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable(self.ice_cream_counter))
        counter = self.driver.find_element(*self.ice_cream_counter)
        counter.click()
        counter.click()

    def click_confirmation_service_button(self):
        WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable(self.service_confirmation_button))
        self.driver.find_element(*self.service_confirmation_button).click()



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_taxi_and_comfort_rate(self):
        rate_page = UrbanRoutesPage(self.driver)
        rate_page.click_taxi_button()
        rate_page.click_comfort_button()

    def test_phone_interaction_and_filling(self):
        form_page = UrbanRoutesPage(self.driver)
        form_page.click_phone_interaction()
        number_phone = data.phone_number
        form_page.filling_phone_field(number_phone)
        assert form_page.get_phone() == number_phone

    def test_phone_code_confirmation(self):
        phone_form = UrbanRoutesPage(self.driver)
        phone_form.click_next_button_after_phone_filling()
        code = retrieve_phone_code(self.driver)
        phone_form.filling_phone_confirmation_code(code)
        phone_form.click_confirm_button_after_code_filling()

    def test_card_interactions_and_filling(self):
        card_form = UrbanRoutesPage(self.driver)
        card_form.click_add_payment_button()
        card_form.click_add_card_button()
        card_data = data.card_number
        cvv_code = data.card_code
        card_form.filling_card_field(card_data)
        card_form.filling_cvv_field(cvv_code)
        assert card_form.get_card_number() == card_number
        assert card_form.get_cvv_number() == card_code
        card_form.click_add_card_confirmation_button()
        card_form.click_close_card_add_interaction(2)

    def test_comments_to_the_driver(self):
        comments_form = UrbanRoutesPage(self.driver)
        comment = data.message_for_driver
        comments_form.add_comment_to_driver(comment)
        assert comments_form.get_comment_to_driver() == comment

    def test_extra_requests(self):
        requests_form = UrbanRoutesPage(self.driver)
        requests_form.click_switch_blanket()
        requests_form.add_ice_cream()

    def test_confirm_service_request(self):
        service_confirmation = UrbanRoutesPage(self.driver)
        service_confirmation.click_confirmation_service_button()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

