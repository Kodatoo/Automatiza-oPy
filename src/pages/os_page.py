import time
from datetime import datetime
from selenium.webdriver.common.by import By
import pyautogui
import os
from openpyxl import load_workbook
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def navegar_para_ordem_servico(driver):
    ordem_de_servico = driver.find_element(By.ID, "menu_35")
    ordem_de_servico.click()
    time.sleep(15)

    consultar_os = driver.find_element(By.ID, "si255")
    consultar_os.click()
    time.sleep(15)

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


def botao_Excel(driver, iframe_selector="iframe", timeout=70):
   

    try:
        print("Aguardando botão de exportação...")
        botao = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#containerBIOSPrincipalGridList__gridArrayContainer > div > div.dx-datagrid-header-panel > div > div > div.dx-toolbar-after > div:nth-child(3) > div > div"
            ))
        )
        print("Botão encontrado. Clicando...")
        botao.click()
        print("Exportação iniciada com sucesso.")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Erro ao localizar ou clicar no botão: {e}")

def botao_Hora(driver, timeout=70):
    try:
        print("Aguardando botão de exportação de horas...")
        botao = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#containerPorHoraGridList__gridArrayContainer > div > div.dx-datagrid-header-panel > div > div > div.dx-toolbar-after > div:nth-child(2) > div > div"
            ))
        )
        print("Botão de horas encontrado. Clicando...")
        botao.click()
        print("Exportação de horas iniciada com sucesso.")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"[ERRO] Erro ao localizar ou clicar no botão de horas: {e}")



