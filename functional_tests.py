from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class SearchSubstituteTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_search_substitute_and_add_favorite(self):
        # user check out homepage
        self.browser.get('http://localhost:8000')
        self.assertIn('Pur beurre', self.browser.title)

        # users click on authenticate menu
        authenticate_link = (self.browser
                             .find_element_by_class_name('fa-sign-in-alt'))
        authenticate_link.click()

        # he notices the title says "Se connecter"
        auth_title = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Se connecter', auth_title)

        # he fills authentication form and hit enter
        mail_box = self.browser.find_element_by_id('id_username')
        mail_box.send_keys('test@test.test')
        password_box = self.browser.find_element_by_id('id_password')
        password_box.send_keys('test')
        password_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # he checks message then he goes back on homepage
        message = (self.browser
                   .find_element_by_id('authentication_message').text)
        self.assertIn('Vous êtes connecté', message)
        homepage_link = self.browser.find_element_by_id('title')
        homepage_link.click()

        # he notices the page title mention purbeurre
        title = self.browser.find_element_by_id('title').text
        self.assertIn('Pur Beurre', title)

        # there is a search box with some suggested products example
        searchbox = self.browser.find_element_by_id('index_search_input')
        self.assertEqual(
            searchbox.get_attribute('placeholder'),
            'ex: Nutella, coca-cola,...'
        )

        # he types "coca cola" in the search box
        searchbox.send_keys('coca-cola')

        # when he hit enter, the page updates, and there are substitute
        # products displayed and the banner product is coca-cola
        searchbox.send_keys(Keys.ENTER)
        time.sleep(1)

        search_product_name = (self.browser
                               .find_element_by_class_name('search_title'))
        self.assertIn('Coca-Cola', search_product_name.text)
        results = self.browser.find_element_by_class_name('results-section')
        products = results.find_elements_by_class_name('product')
        self.assertTrue(len(products) > 0)

        # when the user click on the first proposed substitute
        # he is redirected to the product detail page
        search_first_result_displayed_name = (
            products[0].find_element_by_id('product_name').text)
        products[0].click()
        time.sleep(1)

        product_name = (self.browser
                        .find_element_by_class_name('search_title').text)
        self.assertIn(product_name.upper(), search_first_result_displayed_name)

        # the user click on the save button
        save_button = self.browser.find_element_by_class_name('set_favorite')
        save_button.click()
        time.sleep(1)
        delete_button = self.browser.find_element_by_class_name('set_favorite')
        self.assertIn('Retirer des favoris', delete_button.text)

        # the user then goes on his favorites page
        # and verify the product he saved is there
        favorites_link = self.browser.find_element_by_class_name('fa-carrot')
        favorites_link.click()
        time.sleep(1)
        title = self.browser.find_element_by_class_name('title').text
        self.assertIn('Mes produits favoris', title)
        favorites = self.browser.find_elements_by_class_name('favorite')
        self.assertIn(
            product_name.upper(),
            favorites[-1].find_element_by_class_name('favorite_name').text)

        # the user delete the product from his favorites
        # and checks there are no products left in favorites
        favorites_count = len(favorites)
        delete_button = (favorites[-1]
                         .find_element_by_class_name('remove_favorite'))
        delete_button.click()
        time.sleep(1)
        favorites = self.browser.find_elements_by_class_name('favorite')
        self.assertEqual(favorites_count - 1, len(favorites))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
