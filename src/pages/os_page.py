import time
from datetime import datetime
from selenium.webdriver.common.by import By
import pyautogui
import os
from openpyxl import load_workbook
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
import shutil


def esperar_e_mover_excel(destino, nome_final=None, timeout=60):

    pasta_downloads = r"C:\Users\Administrator\Downloads"
    tempo_inicial = time.time()

    print(f"Aguardando download de Excel para mover para: {destino}")

    while True:
        try:
            arquivos = [f for f in os.listdir(pasta_downloads) if f.lower().endswith(".xlsx")]
        except FileNotFoundError:
            print(f"[ERRO] Pasta de downloads não encontrada: {pasta_downloads}")
            return False

        if arquivos:
            arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(pasta_downloads, x)), reverse=True)
            arquivo_baixado = arquivos[0]
            caminho_origem = os.path.join(pasta_downloads, arquivo_baixado)

            # Ignora arquivos .crdownload (download incompleto)
            if not arquivo_baixado.lower().endswith(".crdownload"):
                # pequena verificação extra: tamanho está estável?
                try:
                    tamanho1 = os.path.getsize(caminho_origem)
                    time.sleep(0.5)
                    tamanho2 = os.path.getsize(caminho_origem)
                    if tamanho1 == tamanho2:
                        break
                except Exception:
                    # se não conseguir ler tamanho, assume pronto
                    break

        if time.time() - tempo_inicial > timeout:
            print("[ERRO] Timeout esperando download do Excel.")
            return False

        time.sleep(1)

    # criar destino se necessário
    if not os.path.exists(destino):
        os.makedirs(destino, exist_ok=True)

    nome_final = nome_final if nome_final else arquivo_baixado
    caminho_destino = os.path.join(destino, nome_final)

    try:
        shutil.move(caminho_origem, caminho_destino)
        print(f"[OK] '{arquivo_baixado}' movido para: {caminho_destino}")
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao mover o arquivo: {e}")
        return False



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

    destino_final = r"C:\Users\Administrator\Documents\Power BI\Dados\Fato"
    nome_arquivo = "Chamados.xlsx"

    for tentativa in range(tentativas_max):
        try:
            botao = driver.find_element(
                By.XPATH,
                "//i[contains(@class,'dx-icon-export-excel-button')]/ancestor::div[@role='button']"
            )

            if botao.is_enabled() and botao.is_displayed():
                print(f"Botão encontrado na tentativa {tentativa + 1}. Clicando...")
                try:
                    botao.click()
                except (StaleElementReferenceException, ElementClickInterceptedException):
                    try:
                        driver.execute_script("arguments[0].click();", botao)
                    except Exception as e_js:
                        print(f"[ERRO] Falha ao clicar via JS: {e_js}")
                        raise
                print("Exportação iniciada com sucesso.")

                # mover arquivo baixado para destino final
                esperar_e_mover_excel(destino_final, nome_arquivo)
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

    destino_final = r"C:\Users\Administrator\Documents\Power BI\Dados\Fato"
    nome_arquivo = "Atendimentos.xlsx"

    css_selectors = [
        "div.dx-datagrid-export-button.dx-button",
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
        # TENTAR CSS
        for sel in css_selectors:
            try:
                botao = WebDriverWait(driver, timeout_por_tentativa).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                )

                if botao and botao.is_displayed() and botao.is_enabled():
                    try:
                        botao.click()
                    except (StaleElementReferenceException, ElementClickInterceptedException):
                        try:
                            driver.execute_script("arguments[0].click();", botao)
                        except Exception as e_js:
                            print(f"[ERRO] Falha ao clicar via JS (CSS): {e_js}")
                            raise
                    print(f"Botão encontrado pelo CSS '{sel}' na tentativa {tentativa}. Clicado com sucesso.")

                    esperar_e_mover_excel(destino_final, nome_arquivo)
                    return
            except Exception:
                pass

        # TENTAR XPATH
        for sel in xpath_selectors:
            try:
                botao = WebDriverWait(driver, timeout_por_tentativa).until(
                    EC.element_to_be_clickable((By.XPATH, sel))
                )

                if botao and botao.is_displayed() and botao.is_enabled():
                    try:
                        botao.click()
                    except (StaleElementReferenceException, ElementClickInterceptedException):
                        try:
                            driver.execute_script("arguments[0].click();", botao)
                        except Exception as e_js:
                            print(f"[ERRO] Falha ao clicar via JS (XPATH): {e_js}")
                            raise
                    print(f"Botão encontrado pelo XPATH '{sel}' na tentativa {tentativa}. Clicado com sucesso.")

                    esperar_e_mover_excel(destino_final, nome_arquivo)
                    return
            except Exception:
                pass

        # fallback usando ancestor do ícone
        try:
            icones = driver.find_elements(By.CSS_SELECTOR, "i.dx-icon-export-excel-button")
            for elm in icones:
                try:
                    parent = elm.find_element(By.XPATH, "./ancestor::div[contains(@class,'dx-button')][1]")
                    if parent and parent.is_displayed():
                        try:
                            parent.click()
                        except (StaleElementReferenceException, ElementClickInterceptedException):
                            try:
                                driver.execute_script("arguments[0].click();", parent)
                            except Exception:
                                pass
                        print(f"Botão clicado via ancestor do ícone na tentativa {tentativa}.")

                        esperar_e_mover_excel(destino_final, nome_arquivo)
                        return
                except Exception:
                    pass
        except Exception:
            pass

        print(f"Tentativa {tentativa} falhou. Tentando novamente em {espera_entre_tentativas} segundos...")
        time.sleep(espera_entre_tentativas)

    print("Não foi possível localizar o botão após várias tentativas (botao_Excel_2).")
