import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password
from selenium.webdriver.chrome.service import Service as ChromeService


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome(
        service=ChromeService(
            executable_path='C:\\Dev\\PetsCard_25.5.1\\chromedriver.exe'
        )
    )
    pytest.driver.maximize_window()
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield
    pytest.driver.quit()


@pytest.fixture()
def go_to_pets_page():
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    pytest.driver.find_element(
        By.ID, 'email'
    ).send_keys(valid_email)
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'pass'))
    )
    pytest.driver.find_element(
        By.ID, 'pass'
    ).send_keys(valid_password)
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[type='submit']")
        )
    )
    pytest.driver.find_element(
        By.CSS_SELECTOR, 'button[type="submit"]'
    ).click()
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located(
            (By.LINK_TEXT, 'Мои питомцы')
        )
    )
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
