# Avaliação de Modelos de Detecção de Objetos para Visão Computacional Assistiva Embarcada

> Protótipo vestível baseado em Raspberry Pi para detecção de obstáculos e navegação assistiva em ambientes escolares.

Artigo publicado na **REMUNOM** — [ler o artigo completo](https://remunom.ojsbr.com/multidisciplinar/pt_BR/article/view/8023).

Este repositório reúne códigos, cadernos de treinamento e documentação do Trabalho de Conclusão de Curso (TCC) desenvolvido no **Instituto Federal de Educação, Ciência e Tecnologia de São Paulo (IFSP) — Campus Campinas**.

---

## Visão geral

A deficiência visual pode comprometer a mobilidade e a segurança em ambientes dinâmicos. Este projeto investiga se modelos de visão computacional treinados com dados específicos do cenário de aplicação conseguem detectar objetos relevantes para a navegação, mantendo características adequadas a sistemas embarcados.

Foi desenvolvido um protótipo vestível com Raspberry Pi, e diferentes arquiteturas de **detecção de objetos** e **segmentação semântica** foram treinadas e avaliadas em um dataset personalizado com cinco classes. Os modelos **YOLO11n** e **YOLO26** foram selecionados para testes em ambiente conhecido e em ambiente não observado.

---

## Resultados experimentais (resumo do artigo)

| Condição | YOLO11n | YOLO26 |
| :--- | :--- | :--- |
| Ambiente conhecido | Detectou as **5 classes** | mAP@50-95 e confiança mais altos em classes específicas |
| Ambiente não observado | Detectou **3 classes** | Detectou **3 classes** |

Os resultados mostram potencial da abordagem e, ao mesmo tempo, limitações de generalização — reforçando a necessidade de maior diversidade no dataset e de avaliações de desempenho no hardware embarcado.

---

## Arquitetura do sistema

### Hardware (edge computing)
* **Processador:** Raspberry Pi 4 Model B (Raspberry Pi OS)
* **Captura:** Raspberry Pi Camera Module (CSI) ou webcam USB
* **Áudio:** fone de ouvido (P2 / Bluetooth) via `espeak` (pt-BR)
* **Alimentação:** power bank portátil (5V/3A)

### Software
* **Linguagem:** Python 3
* **Vídeo:** OpenCV (`opencv-python`)
* **IA:** Ultralytics (`ultralytics` — YOLO / RT-DETR) e demais frameworks nos notebooks
* **Voz:** `espeak` em thread dedicada (`src/main.py`)

---

## Dataset

Dataset customizado do domínio (corredores escolares) com **5 classes**:

1. `cleaning cart` — Carrinho de limpeza  
2. `fire extinguisher` — Extintor de incêndio  
3. `safety cone` — Cone de segurança  
4. `water fountain` — Bebedouro  
5. `trash can` — Lixeira  

Imagens anotadas e organizadas via **Roboflow**. Exemplos em `assets/`.

---

## Modelos avaliados

Arquiteturas treinadas nos notebooks (`notebooks/`):

| Modelo | Tarefa |
| :--- | :--- |
| YOLO11n / YOLO26 | Detecção |
| RT-DETR-L | Detecção |
| MobileNetV3 + SSD | Detecção / classificação |
| SegFormer | Segmentação |
| U-Net | Segmentação |

Para a avaliação experimental em campo, destacam-se **YOLO11n** (melhor cobertura de classes no ambiente conhecido) e **YOLO26** (melhores mAP@50-95 e confiança em classes isoladas).

---

## Como executar no Raspberry Pi

```bash
# Dependências do sistema (síntese de voz)
sudo apt update && sudo apt install -y espeak

# Ambiente Python
cd src
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Coloque o peso treinado (best.pt) no diretório de execução e rode:
python main.py
```

O script captura frames da câmera, executa inferência YOLO e anuncia por voz os objetos detectados (com intervalo mínimo entre anúncios da mesma classe).

---

## Estrutura do repositório

```text
embedded-assistive-vision/
├── assets/                   # Exemplos de imagens do dataset
├── article/                  # PDF do artigo publicado
├── docs/                     # Anotações e material complementar do TCC
├── notebooks/                # Treinamentos (Google Colab)
│   ├── 01_Treino_Dataset_Yolo11_&_Yolov26.ipynb
│   ├── 02_Treino_Dataset_RT_DETR.ipynb
│   ├── 03_Treino_Dataset_MobileNetV3_+_SSD.ipynb
│   ├── 04_Treino_Dataset_SegFormer.ipynb
│   └── 05_Treino_Dataset_U_Net.ipynb
├── src/
│   ├── main.py               # Captura + inferência + áudio (Raspberry Pi)
│   └── requirements.txt
└── README.md
```

---

## Publicação

**Título:** Avaliação de Modelos de Detecção de Objetos para Visão Computacional Assistiva Embarcada  

**Revista:** REMUNOM  

**Link:** https://remunom.ojsbr.com/multidisciplinar/pt_BR/article/view/8023  

---

## Autores

- **Rafaela Laryssa Mello Neto** — IFSP Campinas ([ORCID](https://orcid.org/0009-0002-9908-8067))
- **Sophia Ferreira Boonen** — IFSP Campinas ([ORCID](https://orcid.org/0009-0002-3849-028X))
- **Glauber da Rocha Balthazar** — IFSP Campinas ([ORCID](https://orcid.org/0000-0002-1993-6621))
