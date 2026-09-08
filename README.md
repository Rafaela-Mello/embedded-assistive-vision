# Visão Assistiva Embarcada com IA (TCC - IFSP)

> **Protótipo vestível baseado em Raspberry Pi para detecção de objetos perigosos e navegação assistiva em ambientes escolares.**

Este repositório contém os códigos, cadernos de treinamento, documentação técnica e análises comparativas do Trabalho de Conclusão de Curso (TCC) desenvolvido no **Instituto Federal de Educação, Ciência e Tecnologia de São Paulo (IFSP)**.

---

## 📌 Visão Geral do Projeto

Pessoas com deficiência visual enfrentam grandes desafios de mobilidade e segurança em ambientes dinâmicos, como corredores escolares, devido a obstáculos estáticos e temporários. 

O objetivo deste projeto é o desenvolvimento de uma tecnologia assistiva vestível (óculos/boné) equipada com uma câmera e uma unidade de processamento embarcada (*Single Board Computer*). O sistema utiliza modelos avançados de **Visão Computacional** e **Inteligência Artificial** para identificar potenciais riscos em tempo real e emitir alertas auditivos ao usuário.

---

## 🛠️ Arquitetura do Sistema

### Hardware (Edge Computing)
* **Processador:** Raspberry Pi 4 Model B+ (Raspberry Pi OS)[cite: 1, 2]
* **Captura de Imagem:** Raspberry Pi Camera Module (Interface CSI)[cite: 1, 2]
* **Saída de Áudio:** Fone de Ouvido (P2 / Bluetooth) para emissão de alertas em tempo real[cite: 1, 2]
* **Alimentação:** Power Bank portátil (5V/3A via USB-C)[cite: 1, 2]

### Software & Bibliotecas
* **Linguagem:** Python 3[cite: 1, 2]
* **Processamento de Vídeo:** OpenCV (`opencv-python`)[cite: 1, 2]
* **Framework de IA:** `ultralytics` (YOLO e RT-DETR) / `transformers`[cite: 1, 2]

---

## 📦 Dataset (Roboflow)

Foi construído um **Custom Dataset** focado no domínio de aplicação (corredores escolares) contemplando 5 classes prioritárias de objetos perigosos/obstáculos[cite: 1, 2]:
1. 🛒 `cleaning cart` (Carrinho de limpeza)[cite: 1, 2]
2. 🧯 `fire extinguisher` (Extintor de incêndio)[cite: 1, 2]
3. ⚠️ `safety cone` (Cone de sinalização)[cite: 1, 2]
4. 🚰 `water fountain` (Bebedouro)[cite: 1, 2]
5. 🗑️ `trash can` (Lixeira)[cite: 1, 2]

> 🔗 **Acesso ao Dataset:** As imagens foram anotadas, pré-processadas e organizadas via plataforma **Roboflow**. *(Adicione aqui o link público do Roboflow se disponível)*[cite: 1, 2].

---

## 📊 Comparação e Avaliação de Modelos

Para fundamentar a escolha do modelo ideal para execução em hardware limitado (Raspberry Pi), foram treinadas e avaliadas seis arquiteturas distintas[cite: 1, 2]:

| Modelo | Tarefa | mAP@50 | mIoU | GFLOPs | F1-Score | Latência | FPS (GPU) | Peso (MB) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLOv11n**[cite: 1] | Detecção[cite: 1] | **0.995**[cite: 1] | - | **6.3**[cite: 1] | 0.9562[cite: 1] | **8.7 ms**[cite: 1] | **94.3**[cite: 1] | **5.5 MB**[cite: 1] |
| **RT-DETR-L**[cite: 1] | Detecção[cite: 1] | **0.995**[cite: 1] | - | 103.5[cite: 1] | **0.9762**[cite: 1] | 23.4 ms[cite: 1] | 41.3[cite: 1] | 66.2 MB[cite: 1] |
| **MobileNetV3**[cite: 1] | Classificação/Det.[cite: 1] | 0.2337[cite: 1] | - | 0.62[cite: 1] | 0.2627[cite: 1] | 33.43 ms[cite: 1] | 29.91[cite: 1] | 13.42 MB[cite: 1] |
| **SegFormer**[cite: 1] | Segmentação[cite: 1] | - | **0.9077**[cite: 1] | 8.4[cite: 1] | 0.9516[cite: 1] | 12.5 ms[cite: 1] | 80.0[cite: 1] | 14.3 MB[cite: 1] |
| **U-Net**[cite: 1] | Segmentação[cite: 1] | - | 0.8776[cite: 1] | 16.5[cite: 1] | 0.9348[cite: 1] | 18.2 ms[cite: 1] | 54.9[cite: 1] | 90 MB[cite: 1] |

### Principais Conclusões dos Testes
* **YOLOv11n vs. YOLO26:** O YOLOv11n demonstrou a melhor cobertura ao detectar todas as 5 classes no corredor original[cite: 1, 2], mantendo baixa latência e leveza computacional[cite: 1, 2]. O YOLO26 apresentou níveis mais altos de confiança em classes isoladas e maior mAP@50-95 no treino, mas pecou na cobertura de classes[cite: 2].
* **Generalização (Ambiente Não Observado):** Em um corredor não presente no treino, a capacidade de detecção caiu para 3 classes em ambos os modelos[cite: 2], evidenciando que fatores de distância e variações visuais exigem maior diversidade no *dataset*[cite: 2].

---

## 📁 Estrutura do Repositório

```text
embedded-assistive-vision/
├── assets/                 # Imagens utilizadas para o treino
├── docs/                     # Artigo e anotações teóricas do TCC
│   ├── anotações_do_tcc.pdf
│   └── artigo_detecção_de_objetos.pdf
├── notebooks/                # Treinamentos executados no Google Colab
│   ├── 01_Treino_Dataset_Yolo11_&_Yolov26.ipynb
│   ├── 02_Treino_Dataset_RT_DETR.ipynb
│   ├── 03_Treino_Dataset_MobileNetV3_+_SSD.ipynb
│   ├── 04_Treino_Dataset_SegFormer.ipynb
│   └── 05_Treino_Dataset_U_Net.ipynb
├── src/                      # Código que roda no Raspberry Pi
│   ├── main.py               # Script principal (Captura + Inferência + Áudio)
│   └── requirements.txt      # Dependências (ultralytics, opencv-python, etc.)
├── models/                   # Pesos otimizados (exportados para inferência)
│   ├── best.pt
└── README.md                 # Página principal do repositório
