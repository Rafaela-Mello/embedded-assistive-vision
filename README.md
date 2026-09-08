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
* **Processador:** Raspberry Pi 4 Model B+ (Raspberry Pi OS)
* **Captura de Imagem:** Raspberry Pi Camera Module (Interface CSI)
* **Saída de Áudio:** Fone de Ouvido (P2 / Bluetooth) para emissão de alertas em tempo real
* **Alimentação:** Power Bank portátil (5V/3A via USB-C)

### Software & Bibliotecas
* **Linguagem:** Python 3
* **Processamento de Vídeo:** OpenCV (`opencv-python`)
* **Framework de IA:** `ultralytics` (YOLO e RT-DETR) / `transformers`

---

## 📦 Dataset (Roboflow)

Foi construído um **Custom Dataset** focado no domínio de aplicação (corredores escolares) contemplando 5 classes prioritárias de objetos perigosos/obstáculos:
1. 🛒 `cleaning cart` (Carrinho de limpeza)
2. 🧯 `fire extinguisher` (Extintor de incêndio)
3. ⚠️ `safety cone` (Cone de sinalização)
4. 🚰 `water fountain` (Bebedouro)
5. 🗑️ `trash can` (Lixeira)

> 🔗 **Acesso ao Dataset:** As imagens foram anotadas, pré-processadas e organizadas via plataforma **Roboflow**. *(Adicione aqui o link público do Roboflow se disponível)*.

---

## 📊 Comparação e Avaliação de Modelos

Para fundamentar a escolha do modelo ideal para execução em hardware limitado (Raspberry Pi), foram treinadas e avaliadas seis arquiteturas distintas:

| Modelo | Tarefa | mAP@50 | mIoU | GFLOPs | F1-Score | Latência | FPS (GPU) | Peso (MB) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLOv11n** | Detecção | **0.995** | - | **6.3** | 0.9562 | **8.7 ms** | **94.3** | **5.5 MB** |
| **RT-DETR-L** | Detecção | **0.995** | - | 103.5 | **0.9762** | 23.4 ms | 41.3 | 66.2 MB |
| **MobileNetV3** | Classificação/Det. | 0.2337 | - | 0.62 | 0.2627 | 33.43 ms | 29.91 | 13.42 MB |
| **SegFormer** | Segmentação | - | **0.9077** | 8.4 | 0.9516 | 12.5 ms | 80.0 | 14.3 MB |
| **U-Net** | Segmentação | - | 0.8776 | 16.5 | 0.9348 | 18.2 ms | 54.9 | 90 MB |

### Principais Conclusões dos Testes
* **YOLOv11n vs. YOLO26:** O YOLOv11n demonstrou a melhor cobertura ao detectar todas as 5 classes no corredor original, mantendo baixa latência e leveza computacional. O YOLO26 apresentou níveis mais altos de confiança em classes isoladas e maior mAP@50-95 no treino, mas pecou na cobertura de classes.
* **Generalização (Ambiente Não Observado):** Em um corredor não presente no treino, a capacidade de detecção caiu para 3 classes em ambos os modelos, evidenciando que fatores de distância e variações visuais exigem maior diversidade no *dataset*.

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
```
