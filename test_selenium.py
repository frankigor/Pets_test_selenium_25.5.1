import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_get_all_pets(go_to_pets_page):
    """Проверяем страницу со списком питомцев."""
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left'))
    )
    pets_statistic = pytest.driver.find_element(
        By.XPATH, '//div[@class=".col-sm-4 left"]'
    ).text.split('\n')[1].split(': ')[1]
    WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr'))
    )
    pets_count = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    assert int(pets_statistic) == len(pets_count)


def test_half_pets_have_photo(go_to_pets_page):
    """Проверка, что хотя бы у половины питомцев есть фото."""
    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements(
        By.XPATH, '//table[@class="table table-hover"]/tbody/tr/th/img'
    )
    images_count = 0
    for image in images:
        if 'base64' in image.get_attribute('src'):
            images_count = images_count + 1
    assert images_count / len(images) >= 0.5


def test_all_pets_have_attribute(go_to_pets_page):
    """Проверка, что у питомцев есть имя, порода, возраст."""
    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements(
        By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]'
    )
    breeds = pytest.driver.find_elements(
        By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[2]'
    )
    ages = pytest.driver.find_elements(
        By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[3]'
    )
    name, breed, age = [names, breeds, ages]
    for i in range(len(name)):
        assert names[i].text is not None
        assert breed[i].text is not None
        assert age[i].text is not None


def test_all_pets_have_different_names(go_to_pets_page):
    """Проверка, что имена питомцев не совпадают."""
    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements(
        By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]'
    )
    list_names = [name.text for name in names]
    set_names = set(list_names)
    assert len(set_names) == len(list_names)


def test_all_pets_different(go_to_pets_page):
    """Проверка, что питомцы не повторяются."""
    pytest.driver.implicitly_wait(10)
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="all_my_pets"]/table/tbody/tr'))
    )
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    pets_data = [pet.text for pet in all_pets]
    uniq_pets = set(pets_data)
    assert len(pets_data) == len(uniq_pets)