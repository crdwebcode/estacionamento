# ParkSul - Gerenciamento de Estacionamento

O **ParkSul** é um aplicativo de gerenciamento de estacionamento desenvolvido em Python com uma interface gráfica construída usando `Tkinter`. Ele permite o controle das vagas, registro de entradas e saídas de veículos, cálculo de tarifas, geração de recibos e QR Codes para pagamento.

---

## 📋 Funcionalidades

- **Controle de Vagas**:
  - Exibição visual das vagas disponíveis e ocupadas.
  - Atualização em tempo real do status das vagas.

- **Registro de Veículos**:
  - Entrada de veículos com registro da placa e horário.
  - Saída de veículos com cálculo de tarifa baseado no tempo de permanência.

- **Cálculo de Tarifas**:
  - Tarifáção automática com base no tempo de uso do estacionamento.

- **Geração de Recibos e QR Codes**:
  - Recibos de pagamento com informações detalhadas.
  - QR Codes para facilitar o pagamento via PIX.

---

## 🚀 Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Bibliotecas**:
  - `Tkinter`: Interface gráfica.
  - `sqlite3`: Banco de dados local para registro de vagas e histórico.
  - `qrcode`: Geração de QR Codes.
  - `Pillow`: Manipulação de imagens para exibir QR Codes.
  - `os`, `time`, `datetime`: Funcionalidades adicionais do Python.

---

## ⚙️ Como Configurar e Executar

1. **Clone este repositório**:
   ```bash
   git clone https://github.com/CRDWEBCODE/ParkSul.git
   cd ParkSul
   ```

2. **Instale as dependências**:
   Certifique-se de que o Python 3 e o `pip` estão instalados. Em seguida, execute:
   ```bash
   pip install qrcode pillow
   ```

3. **Configure o Banco de Dados**:
   Execute o script `initialize_db.py` para criar o banco de dados local:
   ```bash
   python3 initialize_db.py
   ```

4. **Execute o aplicativo**:
   ```bash
   python3 main.py
   ```

---

## 📦 Estrutura do Projeto

```plaintext
ParkSul/
├── build/
├── dist/
├── initialize_db.py   # Script para inicializar o banco de dados
├── main.py            # Arquivo principal do aplicativo
├── main.spec          # Configuração para PyInstaller
├── parking.db         # Banco de dados SQLite
├── qrcodes/           # Diretório para armazenar QR Codes gerados
└── receipts/          # Diretório para armazenar recibos gerados
```

---

## 🛋️ Requisitos

- **Python**: Versão 3.6 ou superior.
- **Dependências**:
  - `qrcode`
  - `Pillow`

---

## 🔖 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 🧑‍💻 Autor

Desenvolvido por **CRDWEBCODE**.

