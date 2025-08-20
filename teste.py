import cv2
import numpy as np

# Função para identificar cor pelo valor HSV
def identify_color(hsv_pixel):
    h, s, v = hsv_pixel

    if s < 50 and v > 200:
        return "Branco"
    if v < 50:
        return "Preto"

    if (h >= 0 and h <= 10) or (h >= 170 and h <= 180):
        return "Vermelho"
    if 10 < h <= 25:
        return "Laranja"
    if 25 < h <= 35:
        return "Amarelo"
    if 35 < h <= 85:
        return "Verde"
    if 85 < h <= 125:
        return "Azul"

    return "Desconhecido"

# Abrir webcam
cap = cv2.VideoCapture(0)

# Definir posições dos 9 quadradinhos (x, y, tamanho)
size = 40
offset = 60
start_x, start_y = 200, 120

positions = []
for row in range(3):
    for col in range(3):
        x = start_x + col * offset
        y = start_y + row * offset
        positions.append((x, y))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_colors = []

    # Desenhar os quadrados e capturar cores
    for (x, y) in positions:
        roi = hsv[y:y+size, x:x+size]
        mean_color = cv2.mean(roi)[:3]  # pega média (H,S,V)
        mean_color = tuple(map(int, mean_color))

        color_name = identify_color(mean_color)
        detected_colors.append(color_name)

        # Desenha o quadrado na tela
        cv2.rectangle(frame, (x, y), (x+size, y+size), (255, 255, 255), 2)
        cv2.putText(frame, color_name, (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

    # Mostra a captura
    cv2.imshow("Detecção de Cubo Mágico", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
