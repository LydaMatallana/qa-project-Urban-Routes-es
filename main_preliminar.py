from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from main import retrieve_phone_code
import time

import data

driver = webdriver.Chrome()
driver.get("https://cnt-e0adf5be-549e-4a02-a72c-230cdb4cb9ec.containerhub.tripleten-services.com?lng=es")

time.sleep(2)

driver.find_element(By.ID, 'from').send_keys(data.address_from)
driver.find_element(By.ID, 'to').send_keys(data.address_to)
driver.find_element(By.ID, 'from').get_property('value')
driver.find_element(By.ID, 'to').get_property('value')
time.sleep(2)
driver.find_element(By.XPATH, '//div[@class="type-picker shown"]/div[@class="results-container"]/div[@class="results-text"]/button').click()
time.sleep(2)
driver.find_element(By.XPATH, '//div[@class="tariff-cards"]/div[5]').click()
time.sleep(2)
# Esta parte de lo del telefono en la parte de ingresar el numero hasta el codigo me la salto para poder mirar los otros pasos porque parece que no funciona cerrar la ventana del codigo
#driver.find_element(By.CLASS_NAME, 'np-text').click()
#time.sleep(3)
#driver.find_element(By.CSS_SELECTOR, '.active .label').click()
#time.sleep(3)
#driver.find_element(By.ID, 'phone').send_keys(data.phone_number)
#time.sleep(3)
#driver.find_element(By.ID, 'phone').get_property('value')
#time.sleep(3)
#driver.find_element(By.XPATH, "//div[@class='section active']//form//div[@class='buttons']//button[@type='submit']").click()
#time.sleep(10)
#driver.find_element(By.ID, 'phone').send_keys(retrieve_phone_code(driver))  Este no funciono, ni tampoco funcionó traer los otros metodos
#los que ya venian prestablecidos
#driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/div[2]/div[1]/button").click()
#time.sleep(3)

driver.find_element(By.CLASS_NAME, 'pp-text').click()
time.sleep(2)
driver.find_element(By.CLASS_NAME, "pp-plus").click()
time.sleep(2)
driver.find_element(By.ID, "number").send_keys(data.card_number)
time.sleep(2)
driver.find_element(By.ID, "number").get_property('value')
time.sleep(2)
driver.find_element(By.XPATH, "//div[@class='card-code-input']//input[@id='code']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//div[@class='card-code-input']//input[@id='code']").send_keys(data.card_code)
time.sleep(2)
driver.find_element(By.XPATH, "//div[@class='card-code-input']//input[@id='code']").get_property('value')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, ".plc").click()
time.sleep(2)
driver.find_element(By.XPATH, "//div[@class='pp-buttons']//button[@type='submit']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[3]/div/label").click()
time.sleep(2)
driver.find_element(By.ID, "comment").send_keys(data.message_for_driver)
time.sleep(2)
driver.find_element(By.ID, "comment").get_property('value')
time.sleep(2)
driver.find_element(By.XPATH, "//div[@class='r-sw-container']/*[contains(text(),'Manta')]/..//div[@class='switch']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//div[contains(text(),'Helado')]/..//div[@class='counter-plus']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//div[contains(text(),'Helado')]/..//div[@class='counter-plus']").click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, ".smart-button-secondary").click()
time.sleep(2)
#El ejercicio de la espera si me queda tiempo lo miro
#WebDriverWait(driver, 35).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".order-header-content")))


driver.quit()