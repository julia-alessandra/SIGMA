# SIGMA - Sistema de Gestão de Matérias Acadêmicas

Trabalho prático final desenvolvido para a disciplina de programação orientada a objetos, ofertada pelo departamento de engenharia elétrica da UFMG.

O sistema automatiza a leitura de percursos curriculares e organiza a progressão acadêmica. 
---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:
* **Python 3.10+**
* **Docker & Docker Compose**
* **Pip** (Gerenciador de pacotes do Python)

---

## Instalação e configuração

Siga os passos abaixo para configurar o ambiente local:

### 1. Configurar o ambiente python
Recomenda-se o uso de um ambiente virtual para isolar as dependências:
```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente
# No Linux:
source venv/bin/activate
# No Windows:
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Dependências do sistema (Linux)
Se estiver utilizando Linux (Ubuntu/Debian), o Tkinter deve ser instalado via gerenciador de pacotes:
```bash
sudo apt update && sudo apt install python3-tk -y
```

### 3. Subir o banco de dados (Docker)
O projeto utiliza **MongoDB**. Para subir a instância do banco:
```bash
docker compose up -d
```
*Nota: Caso ocorra erro de permissão no Linux, utilize `sudo chmod 666 /var/run/docker.sock`.*

---

## Execução

Com o banco de dados rodando e o ambiente virtual ativo, execute o sistema:
```bash
python main.py
```

---

## Formato de dados suportado

O sistema foi projetado especificamente para processar os dados do **SIGA/UFMG**.
* **Origem:** "Consulta a percurso curricular".
* **Formato:** Planilha `.pdf`.

---

## Arquitetura do projeto

* **Backend:** Python com Programação Orientada a Objetos.
* **Database:** MongoDB (rodando via Container Docker).
* **GUI:** Tkinter para interface desktop.
* **Services:** Extração de dados via `pdfplumber`.
