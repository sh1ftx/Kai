#!/bin/bash

# Nome do ambiente virtual
VENV_NAME="kaienv"
PYTHON_VERSION="3.6.15"

# Função para instalar dependências do sistema
install_system_deps() {
    echo "[*] Instalando dependências do sistema..."
    sudo pacman -S --needed base-devel zlib libffi openssl xz tk gdbm readline sqlite ncurses
}

# Função para instalar o Python 3.6.15 via pyenv
install_python() {
    if ! pyenv versions | grep -q "$PYTHON_VERSION"; then
        echo "[*] Instalando Python $PYTHON_VERSION via pyenv..."
        MAKEOPTS="-j$(nproc)" pyenv install $PYTHON_VERSION
    else
        echo "[✓] Python $PYTHON_VERSION já instalado no pyenv."
    fi
}

# Função para criar o virtualenv com pyenv
create_virtualenv() {
    if ! pyenv virtualenvs | grep -q "$VENV_NAME"; then
        echo "[*] Criando ambiente virtual: $VENV_NAME..."
        pyenv virtualenv $PYTHON_VERSION $VENV_NAME
    else
        echo "[✓] Ambiente virtual $VENV_NAME já existe."
    fi
}

# Função para ativar o ambiente no diretório atual
activate_local_env() {
    echo "[*] Ativando ambiente local com pyenv..."
    pyenv local $VENV_NAME
}

# Função para instalar os pacotes necessários
install_python_deps() {
    echo "[*] Instalando dependências Python..."
    pip install --upgrade pip
    pip install SpeechRecognition pyttsx3 pyaudio
}

# Execução em sequência
install_system_deps
install_python
create_virtualenv
activate_local_env
install_python_deps

echo -e "\n[✓] Ambiente '$VENV_NAME' pronto com Python $PYTHON_VERSION e todas as libs instaladas."
