import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from data import phone_number, card_number, card_code


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
    card_confirmation = (By.CLASS_NAME, 'pp-value-text')
    cvv_field = (By.CSS_SELECTOR, 'input[placeholder="12"]')
    add_card_confirmation_button = (By.XPATH, '//button[text()="Agregar"]')
    card_section_button_close = (By.CSS_SELECTOR, 'div.payment-picker.open button.close-button.section-close')
    add_comment = (By.ID, 'comment')
    switch_blanket = (By.CSS_SELECTOR, ".slider.round")
    ice_cream_counter = (By.CSS_SELECTOR, '.counter-plus')
    ice_cream_value = (By.CSS_SELECTOR, '.counter-value')
    counter_value = (By.CSS_SELECTOR, '.counter-value')
    service_confirmation_button = (By.CSS_SELECTOR, '.smart-button-secondary')
    comfort_specs = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1) > div > div.r-sw-label')
    taxi_modal_confirmation = (By.CSS_SELECTOR, '#root > div > div.order')


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

    def get_comfort_specs(self):
        return self.driver.find_element(*self.comfort_specs).get_property('value')

    def click_phone_interaction(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.phone_button))
        self.driver.find_element(*self.phone_button).click()

    def filling_phone_field(self, number_phone):
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(self.phone_field))
        self.driver.find_element(*self.phone_field).send_keys(number_phone)

    def get_phone(self):
        return self.driver.find_element(*self.phone_button).get_property('value')

    def click_next_button_after_phone_filling(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.phone_button_next))
        self.driver.find_element(*self.phone_button_next).click()

    def filling_phone_confirmation_code(self, code):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(self.code_field))
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

    def get_ice_cream_value(self):
        return self.driver.find_element(*self.ice_cream_value).get_property('value')

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