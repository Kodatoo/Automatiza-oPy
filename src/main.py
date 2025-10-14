from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 

chrome_options = Options()

chrome_options.add_experimental_option("detach", True)

# Configura o serviço do ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options) 

driver.get("https://hc.harmonit.com.br/")

time.sleep(5)

botao_email = driver.find_element(By.ID, "user_name")

botao_email.send_keys("thiago.pereira@valltech.com.br")

time.sleep(5)

botao_senha = driver.find_element(By.ID,"password_field" )

botao_senha.send_keys("@vall1717")


