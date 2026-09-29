# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(page_title="Gerador Fibonacci", page_icon="🔢", layout="centered")

st.title("🔢 Gerador de Sequência de Fibonacci")
st.write("Escolha a quantidade de termos que deseja calcular.")

# Entrada de dados interativa com controle numérico
num_repetitions = st.number_input(
    label="Quantidade de repetições/termos:",
    min_value=1,
    value=10,
    step=1,
    help="Insira um número inteiro positivo."
)

if st.button("Gerar Sequência", type="primary"):
    if num_repetitions <= 0:
        st.warning("Por favor, insira um número inteiro positivo.")
    elif num_repetitions == 1:
        fib_sequence = [0]
    elif num_repetitions == 2:
        fib_sequence = [0, 1]
    else:
        fib_sequence = [0, 1]
        while len(fib_sequence) < num_repetitions:
            next_fib = fib_sequence[-1] + fib_sequence[-2]
            fib_sequence.append(next_fib)

    # Exibição dos resultados
    st.success(f"Sequência gerada com {num_repetitions} termos:")
    st.write(fib_sequence)