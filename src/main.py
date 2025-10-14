from navegador.driver_setup import iniciar_driver
from pages.login import fazer_login
from pages.os_page import navegar_para_ordem_servico, preencher_datas

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def main():
    driver = iniciar_driver()
    
    email = "thiago.pereira@valltech.com.br"
    senha = "@vall1717"
    
    fazer_login(driver, email, senha)
    navegar_para_ordem_servico(driver)
    preencher_datas(driver)
    
    # Próximos passos...

if __name__ == "__main__":
    main()
