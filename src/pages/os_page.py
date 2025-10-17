import time
from datetime import datetime
from selenium.webdriver.common.by import By
import pyautogui


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

# Constantes para a coordenada (opcional, mas boa prática)
X_COORD = 1815
Y_COORD = 1008


time.sleep(30)

def clicar_coordenada_pyautogui():
    """
    Move o mouse para a coordenada (X=1815, Y=1008) na tela e clica.
    
    Aviso: Esta função depende da resolução da tela e da posição da janela.
    Recomendado apenas como último recurso de automação.
    """
    
    # Adiciona um pequeno delay de segurança antes de mover o mouse
    # Isso é bom para dar tempo ao sistema para processar
    time.sleep(1) 
    
    try:
        # Move o mouse para a coordenada
        # O argumento 'duration' (duração) é opcional e simula um movimento humano
        pyautogui.moveTo(X_COORD, Y_COORD, duration=0.5)
        time.sleep(15)
        
        # Clica na coordenada atual
        pyautogui.click()
        
        print(f"PyAutoGUI: Mouse movido para ({X_COORD}, {Y_COORD}) e clique realizado.")
        
    except Exception as e:
        print(f"Erro ao executar PyAutoGUI: {e}")
        print("Certifique-se de que o PyAutoGUI está instalado e as permissões estão corretas.")