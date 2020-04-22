from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class SearchSubstituteTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_search_substitute_and_access_detail_page(self):
        # user check out homepage
        self.browser.get('http://localhost:8000')

        # he notices the page title mention purbeurre
        self.assertIn('Pur beurre', self.browser.title)
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

        # when he its enter, the page updates, and there are substitute products displayed and the banner product is coca-cola
        searchbox.send_keys(Keys.ENTER)
        time.sleep(1)

        search_product_name = self.browser.find_element_by_class_name('search_title')
        self.assertIn('Coca-Cola', search_product_name.text)
        results = self.browser.find_element_by_class_name('results-section')
        products = results.find_elements_by_class_name('product')
        self.assertTrue(len(products) > 0)

        # when the user click on the first proposed substitute he is redirected to the product detail page
        search_first_result_displayed_name = products[0].find_element_by_id('product_name').text
        products[0].click()
        time.sleep(1)

        product_name = self.browser.find_element_by_class_name('search_title').text
        self.assertIn(product_name.upper(), search_first_result_displayed_name)



if __name__ == '__main__':
    unittest.main(warnings='ignore')
