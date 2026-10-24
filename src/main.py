"""
Visão Assistiva Embarcada — script de inferência em tempo real.

Captura frames da câmera, detecta obstáculos com YOLO e anuncia
os resultados por voz (espeak), visando uso em Raspberry Pi.
"""

import time
import cv2
import os
import threading
from queue import Queue
from ultralytics import YOLO

# Nomes das classes do dataset customizado (inglês → português para o alerta sonoro)
TRADUCOES = {
    "cleaning cart": "Carrinho de limpeza",
    "fire extinguisher": "Extintor de incêndio",
    "safety cone": "Cone de segurança",
    "trash can": "Lixeira",
    "water fountain": "Bebedouro"
}

# Fila thread-safe: a thread principal enfileira textos; a thread de voz os consome
fila_fala = Queue()


def voz():
    """Consome a fila e sintetiza fala em português com espeak (não bloqueia a inferência)."""
    while True:
        texto = fila_fala.get()
        # Sentinela None encerra a thread de áudio
        if texto is None:
            break
        # -v pt-br: voz em português do Brasil | -s 130: velocidade | -p 40: tom
        os.system(f'espeak -v pt-br -s 130 -p 40 "{texto}"')
        fila_fala.task_done()


def main():
    # Pesos treinados no dataset do domínio (corredores escolares); arquivo best.pt no cwd
    print("Carregando modelo YOLO...")
    model = YOLO("best.pt")

    # Índice 0 = câmera padrão (webcam USB ou módulo CSI no Raspberry Pi)
    print("Carregado a camera...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Não foi possível acessar a câmera.")
        return

    # Resolução reduzida para menor carga de CPU/GPU no dispositivo embarcado
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Áudio em thread separada para não atrasar o loop de detecção
    thread_audio = threading.Thread(target=voz, daemon=True)
    thread_audio.start()

    # Evita repetir o mesmo objeto em sequência (chave = nome da classe)
    ultima_fala = {}

    # Intervalo mínimo (segundos) entre anúncios da mesma classe
    TEMPO_ESPERA = 4

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Não foi possível ler frame da câmera.")
            break

        # Inferência: conf=0.5 filtra detecções fracas; imgsz=320 reduz custo computacional
        results = model.predict(
            source=frame,
            conf=0.5,
            imgsz=320,
            verbose=False
        )

        agora = time.time()

        # Percorre as caixas detectadas e agenda alerta sonoro quando aplicável
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]

            confianca = float(box.conf[0])
            porcentagem = int(confianca * 100)

            # Só anuncia classes do dataset assistivo (ignora rótulos fora do domínio)
            if label in TRADUCOES:
                # Respeita o tempo de espera e evita empilhar falas se a fila já tiver item
                if (label not in ultima_fala or (agora - ultima_fala[label]) > TEMPO_ESPERA):
                    texto = f"{TRADUCOES[label]} com {porcentagem} por cento de certeza"

                    if fila_fala.empty():
                        fila_fala.put(texto)
                        ultima_fala[label] = agora

        # Visualização opcional (útil em desktop; em produção embarcada costuma ficar desligada)
        #annotated_frame = results[0].plot()
        #cv2.imshow("Detector de objetos", annotated_frame)
        #if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
        #    break

    # Encerra a thread de voz e libera recursos da câmera
    fila_fala.put(None)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
