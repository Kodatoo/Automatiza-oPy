from navegador.driver_setup import iniciar_driver
from pages.login import fazer_login
from pages.os_page import navegar_para_ordem_servico, preencher_datas, botao_filtrar, botao_Excel, clicar_botao_por_hora, ungroup_all_data_inicial, botao_Excel_2
from excel_utils.editor import editar_excel_remover_ultima_linha
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def main():
    driver = iniciar_driver()
    
    email = "thiago.pereira@valltech.com.br"
    senha = "@vall1717"
    
    fazer_login(driver, email, senha)
    navegar_para_ordem_servico(driver)
    preencher_datas(driver)
    botao_filtrar(driver)
    botao_Excel(driver)
    editar_excel_remover_ultima_linha()
    clicar_botao_por_hora(driver)
    ungroup_all_data_inicial(driver)
    time.sleep(20)
    botao_Excel_2(driver)

 

if __name__ == "__main__":
    main()
