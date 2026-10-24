import time
import cv2
import os
import threading
from queue import Queue
from ultralytics import YOLO

TRADUCOES = {
    "cleaning cart": "Carrinho de limpeza",
    "fire extinguisher": "Extintor de incêndio",
    "safety cone": "Cone de segurança",
    "trash can": "Lixeira",
    "water fountain": "Bebedouro"
}

fila_fala = Queue()

def voz():
    while True:
        texto = fila_fala.get()
        if texto is None:
            break
        os.system(f'espeak -v pt-br -s 130 -p 40 "{texto}"')
        fila_fala.task_done()
        
def main():
    # Carrega o modelo YOLOv8 pré-treinado no COCO
    print("Carregando modelo YOLO...")
    model = YOLO("best.pt")

    # Abre a webcam (0 = webcam padrão)
    print("Carregado a camera...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Não foi possível acessar a câmera.")
        return

    # Configura a resolução (opcional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    thread_audio = threading.Thread(target=voz, daemon=True)
    thread_audio.start()

    # Dicionario para controlar o tempo da ultima vez que cada objeto foi anunciado
    ultima_fala = {}
    
    TEMPO_ESPERA = 4

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Não foi possível ler frame da câmera.")
            break

        # Inferência sem filtro de classes
        results = model.predict(
            source=frame,
            conf=0.5,
            imgsz=320,
            verbose=False
        )
        
        agora = time.time()
        
        # Logica da Voz
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            
            confianca = float(box.conf[0])
            porcentagem = int(confianca * 100)
            
            if label in TRADUCOES:
                if (label not in ultima_fala or (agora - ultima_fala[label]) > TEMPO_ESPERA):
                    texto = f"{TRADUCOES[label]} com {porcentagem} por cento de certeza"
                    
                    if fila_fala.empty():
                        fila_fala.put(texto)
                        ultima_fala[label] = agora
        
        # Anota o frame automaticamente
        #annotated_frame = results[0].plot()

        # Exibe o resultado
        #cv2.imshow("Detector de objetos", annotated_frame)

        #if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
        #    break

    fila_fala.put(None)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
