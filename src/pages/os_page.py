import time
from datetime import datetime
from selenium.webdriver.common.by import By

def navegar_para_ordem_servico(driver):
    ordem_de_servico = driver.find_element(By.ID, "menu_35")
    ordem_de_servico.click()
    time.sleep(5)

    consultar_os = driver.find_element(By.ID, "si255")
    consultar_os.click()
    time.sleep(5)

def preencher_datas(driver):
    campos_data = driver.find_elements(By.CLASS_NAME, "dx-texteditor-input")
    
    if len(campos_data) >= 2:
        data_inicial = "01062025"
        data_final = datetime.now().strftime("%d%m%Y")  # sem barras

        campos_data[0].clear()
        campos_data[0].send_keys(data_inicial)
        time.sleep(2)

        campos_data[1].clear()
        campos_data[1].send_keys(data_final)
        time.sleep(2)
    else:
        print("[ERRO] Campos de data não encontrados.")

def botao_filtrar(driver):
    filtros = driver.find_element(By.CLASS_NAME, "uk-button")
    filtros.click()