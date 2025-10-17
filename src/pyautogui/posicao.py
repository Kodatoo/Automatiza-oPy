import pyautogui
import time

print("?? Mova o mouse sobre o ponto desejado. Pressione Ctrl+C para parar.")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Posição: x={x}, y={y}", end="\r")  # Atualiza na mesma linha
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n?? Parado pelo usuário.") #1815 1008