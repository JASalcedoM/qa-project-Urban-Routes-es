import time

import data
import helper
from selenium import webdriver


import UrbanRoutesPage
from data import phone_number, card_number, card_code


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
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_taxi_and_comfort_rate(self):
        rate_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        rate_page.click_taxi_button()
        rate_page.click_comfort_button()
        assert rate_page.get_comfort_specs() == 'Manta y pañuelos'

    def test_phone_interaction_and_filling(self):
        form_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        form_page.click_phone_interaction()
        number_phone = data.phone_number
        form_page.filling_phone_field(number_phone)
        assert form_page.get_phone() == number_phone

    def test_phone_code_confirmation(self):
        phone_form = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        phone_form.click_next_button_after_phone_filling()
        code = helper.retrieve_phone_code(self.driver)
        phone_form.filling_phone_confirmation_code(code)
        phone_form.click_confirm_button_after_code_filling()

    def test_card_interactions_and_filling(self):
        card_form = UrbanRoutesPage.UrbanRoutesPage(self.driver)
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
        comments_form = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        comment = data.message_for_driver
        comments_form.add_comment_to_driver(comment)
        assert comments_form.get_comment_to_driver() == comment

    def test_blanket_request(self):
        requests_form = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        requests_form.click_switch_blanket()
        assert requests_form.switch_blanket.is_selected() == True


    def test_ice_cream_request(self):
        requests_form = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        requests_form.add_ice_cream()
        assert requests_form.get_ice_cream_value() == 2

    def test_wait_for_taxi_modal_to_be_displayed(self):
        service_confirmation = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        service_confirmation.click_confirmation_service_button()
        #Modificación --------------------
        modal = service_confirmation.modal_is_triggered()
        assert modal.is_displayed()



    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

