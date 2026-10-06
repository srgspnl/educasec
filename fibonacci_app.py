# -*- coding: utf-8 -*-
"""Sequência de Fibonacci em Streamlit.

Adaptado do notebook Fibonacci.ipynb (Google Colab).
Para executar:
    pip install streamlit pandas
    streamlit run fibonacci_app.py
"""

import pandas as pd
import streamlit as st


def gerar_fibonacci(n: int) -> list[int]:
    """Retorna os n primeiros termos da sequência de Fibonacci (começando em 0)."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


st.set_page_config(page_title="Fibonacci", page_icon="🌀")
st.title("🌀 Sequência de Fibonacci")
st.write("Cada termo é a soma dos dois anteriores: 0, 1, 1, 2, 3, 5, 8, …")

n = st.number_input(
    "Quantos termos da sequência deseja gerar?",
    min_value=1,
    max_value=1000,
    value=10,
    step=1,
)

if st.button("Gerar sequência", type="primary"):
    seq = gerar_fibonacci(int(n))

    st.subheader("Resultado")
    st.code(", ".join(map(str, seq)), language=None)

    col1, col2 = st.columns(2)
    col1.metric("Termos gerados", len(seq))
    col2.metric("Último termo", f"{seq[-1]:,}".replace(",", "."))

    # Razão entre termos consecutivos: tende à razão áurea (≈ 1,618)
    razoes = [None] + [
        seq[i] / seq[i - 1] if seq[i - 1] else None for i in range(1, len(seq))
    ]
    posicoes = range(1, len(seq) + 1)

    # Os termos crescem além do limite de 64 bits; na tabela vão como texto
    tabela = pd.DataFrame(
        {"Posição": posicoes, "Valor": [str(v) for v in seq], "Razão Fₙ / Fₙ₋₁": razoes}
    )
    grafico = pd.DataFrame(
        {"Valor": [float(v) for v in seq], "Razão": razoes}, index=posicoes
    )

    aba_tabela, aba_grafico = st.tabs(["Tabela", "Gráfico"])
    with aba_tabela:
        st.dataframe(tabela, hide_index=True)
    with aba_grafico:
        st.line_chart(grafico["Valor"])
        if len(seq) > 2:
            st.caption("Razão entre termos consecutivos (converge para φ ≈ 1,618):")
            st.line_chart(grafico["Razão"])
