from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Mantém o navegador aberto após o script terminar
    
    # Configura o serviço do ChromeDriver automaticamente
    service = Service(ChromeDriverManager().install())
    
    # Inicializa o driver do Chrome com as opções e serviço configurados
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver
