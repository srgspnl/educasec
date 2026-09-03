# app.py

import streamlit as st

# Importa as funções que contêm as lógicas de cada cifra/módulo
from cesar import app as cesar_app
from vigenere import app as vigenere_app
from rsa import app as rsa_app
from hash import app as hash_app

def sobre_app():
    st.markdown("### Sobre o Projeto")
    st.write(
        "Bem-vindo à plataforma de estudos e testes criptográficos. "
        "Aqui você encontra demonstrações interativas de cifras históricas e conceitos modernos de criptografia."
    )
    st.info("Utilize o menu lateral para navegar entre os diferentes algoritmos.")

# Configuração da página principal
st.set_page_config(
    page_title="App de Cifras",
    layout="wide"
)

# ----------------- BARRA LATERAL (SIDEBAR) -----------------
st.sidebar.title("Navegação")

# Opções correspondentes ao wireframe: Sobre (saiba mais), César, Vigenère, RSA e Hash
menu_opcoes = [
    "Sobre / Saiba mais...",
    "César",
    "Vigenère",
    "RSA",
    "Hash"
]

opcao_selecionada = st.sidebar.radio(
    "Selecione uma seção:",
    menu_opcoes
)

# ----------------- ÁREA PRINCIPAL (CONTEÚDO) -----------------
# Cabeçalho baseado na anotação superior do wireframe ("CIFRA jogue...")
if opcao_selecionada == "Sobre / Saiba mais...":
    st.title("CIFRA — Saiba mais...")
else:
    st.title(f"CIFRA — {opcao_selecionada} (Jogue / Interaja)")

# Container central ("EXIBE CIFRA") delimitado com borda
with st.container(border=True):
    if opcao_selecionada == "Sobre / Saiba mais...":
        sobre_app()
    elif opcao_selecionada == "César":
        cesar_app()
    elif opcao_selecionada == "Vigenère":
        vigenere_app()
    elif opcao_selecionada == "RSA":
        rsa_app()
    elif opcao_selecionada == "Hash":
        hash_app()