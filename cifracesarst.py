# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(page_title="Cifra de César", page_icon="🔐", layout="centered")

def caesar_cipher(text: str, shift: int) -> str:
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result += shifted_char
        else:
            result += char
    return result

st.title("🔐 Cifra de César")
st.write("Criptografe ou decifre mensagens ajustando o deslocamento do alfabeto.")

# Entrada de texto do usuário
input_text = st.text_area(
    label="Texto para criptografar/processar:",
    placeholder="Digite sua mensagem aqui...",
    height=120
)

# Barra deslizante para definir o deslocamento (de 1 a 25 caracteres)
shift_value = st.slider(
    label="Deslocamento de caracteres (chave):",
    min_value=1,
    max_value=25,
    value=3,
    step=1,
    help="Define quantas posições no alfabeto cada letra será deslocada."
)

if input_text:
    encrypted_text = caesar_cipher(input_text, shift_value)

    st.subheader("Resultado:")
    st.code(encrypted_text, language=None)

    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"**Deslocamento aplicado:** {shift_value}")
    with col2:
        st.caption(f"**Total de caracteres:** {len(input_text)}")
else:
    st.info("Digite algum texto acima para ver o resultado cifrado em tempo real.")