from django.test import LiveServerTestCase
from selenium import webdriver
# from .base import FunctionalTest, wait
from users.models import User
from selenium.webdriver.common.keys import Keys

executable_path = "/home/gai/Desktop/Dev/tdd_python/geckodriver"
from time import sleep


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn



class LoginTest(LiveServerTestCase):

    def setUp(self):
        # Run browser
        self.browser = webdriver.Firefox(executable_path=executable_path)

    # def tearDown(self):
    #     sleep(5)
    #     self.browser.quit()

    # @wait
    # def wait_to_be_logged_in(self):
    #     navbar = self.browser.find_element_by_css_selector('.navbar')
    #     navbar.find_element_by_link_text('Logout')

    # @wait
    # def wait_to_be_logged_out(self):
    #     navbar = self.browser.find_element_by_css_selector('.navbar')
    #     navbar.find_element_by_link_text('Sign in')

    def test_can_login(self):

        # [fixture] sample user is registered
        TEST_USERNAME = 'darius'
        TEST_EMAIL = 'darius@daru.com'
        TEST_PASSWORD = 'qqqqq11111'
        User.objects.create_user(username=TEST_USERNAME,
                                 email=TEST_EMAIL,
                                 password=TEST_PASSWORD)
        ucount = User.objects.count()
        self.assertEqual(1,ucount)

        # John open home page and obviously he is not logged
        self.browser.get(self.live_server_url)
        # self.wait_to_be_logged_out()

        # He clicks 'Sing in' link
        # self.browser.find_element_by_link_text('Signup here').click()
        # self.browser.find_element_by_name('Login').click

        # Then he enter account credentials
        self.browser.find_element_by_name('username').send_keys(TEST_USERNAME)
        sleep(5)
        self.browser.find_element_by_name('password').send_keys(TEST_PASSWORD)
        sleep(5)
        self.browser.find_element_by_name('password').send_keys(Keys.ENTER)
        

        # John is logged in
        # self.wait_to_be_logged_in()