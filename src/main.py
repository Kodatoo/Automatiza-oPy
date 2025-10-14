from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 



chrome_options = Options()

chrome_options.add_experimental_option("detach", True)

# Configura o serviço do ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options) 

driver.get("https://hc.harmonit.com.br/")

driver.maximize_window()

time.sleep(5)

botao_email = driver.find_element(By.ID, "user_name")

botao_email.send_keys("thiago.pereira@valltech.com.br")

time.sleep(5)

botao_senha = driver.find_element(By.ID,"password_field" )

botao_senha.send_keys("@vall1717")

time.sleep(5)

botao_confirmar = driver.find_element(By.ID, "btn_login")

botao_confirmar.click()

time.sleep(5)

ordem_de_serviço = driver.find_element(By.ID, "menu_35")
ordem_de_serviço.click()

time.sleep(5)

consultar_os = driver.find_element(By.ID, "si255")
consultar_os.click()

time.sleep(5)

data_incicial = driver.find_element(By.CLASS_NAME, "dx-texteditor-input")
data_incicial.send_keys("01062025")

time.sleep(5)

data_atual = datetime.now().strftime("%d/%m/%Y")

data_final = driver.find_element(By.CLASS_NAME, "dx-texteditor-input")
data_final.send_keys(data_atual)