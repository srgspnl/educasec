# app.py
import streamlit as st
# Importa as funções que contêm as lógicas de cada cifra
from cesar import app as cesar_app
from vigenere import app as vigenere_app
from enigma import app as enigma_app
from rsa import app as rsa_app
from hash import app as hash_app
from ecc import app as ecc_app
# Configuração da página principal
st.set_page_config(
    page_title="App de Cifras",
    layout="wide"
)
# Cria o menu na barra lateral
st.sidebar.title("Navegação")
opcao_selecionada = st.sidebar.radio(
    "Escolha a cifra:",
    ("Cifra de César", "Cifra de Vigenère", "Enigma", "RSA", "ECC", "Hash")
)
# Lógica para exibir a página correta
if opcao_selecionada == "Cifra de César":
    cesar_app()
elif opcao_selecionada == "Cifra de Vigenère":
    vigenere_app()
elif opcao_selecionada == "Enigma":
    enigma_app()
elif opcao_selecionada == "RSA":
    rsa_app()
elif opcao_selecionada == "ECC":
    ecc_app()
elif opcao_selecionada == "Hash":
    hash_app()
st.sidebar.markdown("---")
st.sidebar.info("Escolha uma cifra no menu acima para começar.")
