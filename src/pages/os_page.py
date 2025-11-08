import time
from datetime import datetime
from selenium.webdriver.common.by import By
import pyautogui
import os
from openpyxl import load_workbook
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains



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


def botao_Excel(driver, tentativas_max=30, espera_entre_tentativas=2):
    print("Procurando botão de exportação...")

    for tentativa in range(tentativas_max):
        try:
            botao = driver.find_element(By.CSS_SELECTOR,
                "#containerBIOSPrincipalGridList__gridArrayContainer > div > div.dx-datagrid-header-panel > div > div > div.dx-toolbar-after > div:nth-child(3) > div > div"
            )
            if botao.is_enabled() and botao.is_displayed():
                print(f"Botão encontrado na tentativa {tentativa + 1}. Clicando...")
                botao.click()
                print("Exportação iniciada com sucesso.")
                return
        except Exception:
            pass

        print(f"Tentativa {tentativa + 1} falhou. Tentando novamente em {espera_entre_tentativas} segundos...")
        time.sleep(espera_entre_tentativas)

    print("Não foi possível localizar o botão após várias tentativas.")

def clicar_botao_por_hora(driver, timeout=20):
    """
    Localiza e clica na aba 'Por Hora' usando XPath baseado no texto.
    Funciona mesmo se o ID do elemento mudar (DevExpress).
    """

    try:
        botao_por_hora = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(., 'Por Hora')]")
            )
        )
        botao_por_hora.click()
        print("[OK] Botão 'Por Hora' clicado com sucesso.")
    except Exception as e:
        print("[ERRO] Não foi possível clicar no botão 'Por Hora':", e)




def ungroup_all_data_inicial(driver, timeout=20):
    try:
        wait = WebDriverWait(driver, timeout)

        # 1. Localiza a coluna Data Inicial
        coluna = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'dx-datagrid-text-content') and contains(.,'Data Inicial')]")
            )
        )

        # 2. Clique direito
        ActionChains(driver).context_click(coluna).perform()
        print("[OK] Clique direito realizado.")

        # 3. Espera o submenu visível aparecer
        submenu = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='dx-submenu' and contains(@style,'visibility: visible')]")
            )
        )

        # 4. Agora pega o Ungroup All dentro do submenu visível
        ungroup = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='dx-submenu' and contains(@style,'visibility: visible')]"
                    "//span[normalize-space()='Ungroup All']"
                )
            )
        )

        ungroup.click()
        print("[OK] 'Ungroup All' clicado com sucesso.")

    except Exception as e:
        print("[ERRO] Falha ao executar 'Ungroup All':", e)
