from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest
from time import sleep

# ######common functions########

def launch_swaglabs():
    global driver
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.saucedemo.com/')

def valid_login_swaglabs():
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.NAME, 'password').send_keys('secret_sauce')
    driver.find_element(By.CLASS_NAME, 'submit-button').click()

def capture_evidence():
    image_name = fr"C:\pytest-basics\evidence\image-{datetime.today().strftime('%m%d%y-%H%M%S')}.png"
    driver.save_screenshot(image_name)

def text_is_displayed(text):
    return text.lower() in driver.page_source.lower()

def add_item_to_cart():
    add_item=driver.find_elements(By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")
    add_item[0].click()

def click_shopping_cart():
    driver.find_elements(By.ID, 'shopping_cart_container')


############### Test Cases ##############

def test_launch_login_page():
    launch_swaglabs()
    assert driver.title == 'Swag Labs'
    capture_evidence()
    driver.quit()

login_form_parameters = [
    ('locked_out_user', 'secret_sauce', 'Sorry, this user has been locked out'),
    ('test',             'test',          'Username and password do not match any user in this service')
] 


@pytest.mark.parametrize("username, password, checkpoint", login_form_parameters)
def test_login_invalid_credentials(username, password, checkpoint):
    launch_swaglabs()
    driver.find_element(By.ID, 'user-name').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'submit-button').click()
    sleep(5)
    assert text_is_displayed(checkpoint)
    capture_evidence()
    driver.quit()

##############BELOW TEST CASES PASS###############################
@pytest.fixture()
def setup(request):
    launch_swaglabs()
    valid_login_swaglabs()
    

    def teardown():
        capture_evidence()
        driver.quit()
    request.addfinalizer(teardown)

def test_login_valid_credentials(setup):
    assert text_is_displayed('products')
   
def test_view_product_details(setup):
    product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
    product_names[0].click()
    assert text_is_displayed('back to products')
  

def test_add_item_to_cart(setup):
    add_item_to_cart()
    click_shopping_cart()
    assert text_is_displayed('Add to cart')