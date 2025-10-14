import time
from selenium.webdriver.common.by import By

def fazer_login(driver, email, senha):
    driver.get("https://hc.harmonit.com.br/")
    driver.maximize_window()
    time.sleep(5)

    botao_email = driver.find_element(By.ID, "user_name")
    botao_email.send_keys(email)
    time.sleep(2)

    botao_senha = driver.find_element(By.ID, "password_field")
    botao_senha.send_keys(senha)
    time.sleep(2)

    botao_confirmar = driver.find_element(By.ID, "btn_login")
    botao_confirmar.click()
    time.sleep(5)
