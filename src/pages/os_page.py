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
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
import time


def navegar_para_ordem_servico(driver):
    ordem_de_servico = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[.//span[contains(text(),'Ordem de Serviço')]]")
        )
    )
    ordem_de_servico.click()
    time.sleep(2)

    consultar_os = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'Consultar') or contains(text(),'Consulta')]")
        )
    )
    consultar_os.click()
    time.sleep(2)
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
            botao = driver.find_element(
                By.XPATH,
                "//i[contains(@class,'dx-icon-export-excel-button')]/ancestor::div[@role='button']"
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

    
        coluna = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'dx-datagrid-text-content') and contains(.,'Data Inicial')]")
            )
        )

      
        ActionChains(driver).context_click(coluna).perform()
        print("[OK] Clique direito realizado.")

      
        submenu = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='dx-submenu' and contains(@style,'visibility: visible')]")
            )
        )

    
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



def botao_Excel_2(driver, tentativas_max=30, espera_entre_tentativas=2, timeout_por_tentativa=5):

    print("Procurando botão de exportação (botao_Excel_2)...")


    css_selectors = [
        "div.dx-datagrid-export-button.dx-button",  # classe principal
        "div[aria-label='export-excel-button']",
        "div[title*='Exportar dados']",
        "div.dx-datagrid-toolbar-button.dx-datagrid-export-button",
        "div.dx-datagrid-export-button", 
    ]
    xpath_selectors = [
        "//div[contains(@class,'dx-datagrid-export-button') and descendant::i[contains(@class,'dx-icon-export-excel-button')]]",
        "//div[@aria-label='export-excel-button']",
        "//div[contains(@title,'Exportar dados') or contains(@aria-label,'export-excel-button')]",
        "//i[contains(@class,'dx-icon-export-excel-button')]/parent::div/parent::div"
    ]

    for tentativa in range(1, tentativas_max + 1):
        for sel in css_selectors:
            try:
              
                try:
                    botao = WebDriverWait(driver, timeout_por_tentativa).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                    )
                except TimeoutException:
                    botao = None

                if botao and botao.is_displayed() and botao.is_enabled():
                    try:
                        botao.click()
                        print(f"Botão encontrado pelo CSS '{sel}' na tentativa {tentativa}. Clicado com sucesso.")
                        return
                    except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                        # tentar clicar via JS como fallback
                        try:
                            driver.execute_script("arguments[0].click();", botao)
                            print(f"Clique via JS realizado (CSS '{sel}') na tentativa {tentativa}.")
                            return
                        except Exception as e2:
                            print(f"Falha ao clicar (CSS '{sel}') via JS: {e2}")
                          
            except Exception:
                pass

       
        for sel in xpath_selectors:
            try:
                try:
                    botao = WebDriverWait(driver, timeout_por_tentativa).until(
                        EC.element_to_be_clickable((By.XPATH, sel))
                    )
                except TimeoutException:
                    botao = None

                if botao and botao.is_displayed() and botao.is_enabled():
                    try:
                        botao.click()
                        print(f"Botão encontrado pelo XPATH '{sel}' na tentativa {tentativa}. Clicado com sucesso.")
                        return
                    except (StaleElementReferenceException, ElementClickInterceptedException):
                        try:
                            driver.execute_script("arguments[0].click();", botao)
                            print(f"Clique via JS realizado (XPATH '{sel}') na tentativa {tentativa}.")
                            return
                        except Exception as e2:
                            print(f"Falha ao clicar (XPATH '{sel}') via JS: {e2}")
            except Exception:
                pass

        try:
            icone = driver.find_elements(By.CSS_SELECTOR, "i.dx-icon-export-excel-button")
            for elm in icone:
                try:
                    parent = elm.find_element(By.XPATH, "./ancestor::div[contains(@class,'dx-button')][1]")
                    if parent and parent.is_displayed():
                        try:
                            parent.click()
                            print(f"Botão clicado via ancestor do ícone na tentativa {tentativa}.")
                            return
                        except Exception:
                            try:
                                driver.execute_script("arguments[0].click();", parent)
                                print(f"Clique via JS no ancestor do ícone na tentativa {tentativa}.")
                                return
                            except Exception:
                                pass
                except Exception:
                    pass
        except Exception:
            pass

        # se não encontrou nada, espera e tenta novamente
        print(f"Tentativa {tentativa} falhou. Tentando novamente em {espera_entre_tentativas} segundos...")
        time.sleep(espera_entre_tentativas)

    print("Não foi possível localizar o botão após várias tentativas (botao_Excel_2).")


