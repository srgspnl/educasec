# app2.py

import streamlit as st

# Importa as funções que contêm as lógicas de cada cifra
from cesar import app as cesar_app
from vigenere import app as vigenere_app
from enigma import app as enigma_app
from rsa import app as rsa_app
from hash import app as hash_app

# ------------------------------------------------------------------
# Configuração da página principal
# ------------------------------------------------------------------
st.set_page_config(
    page_title="App de Cifras",
    page_icon="🔐",
    layout="wide"
)

# ------------------------------------------------------------------
# CSS customizado — deixa os botões em formato de pílula e dá um
# acabamento de "cartão" mais próximo do rascunho
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Botões do menu em formato de pílula, ocupando a largura da coluna */
    div[data-testid="stButton"] > button {
        border-radius: 999px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.15s ease-in-out;
    }
    /* Botão "secundário" (não selecionado): contorno discreto */
    div[data-testid="stButton"] > button[kind="secondary"] {
        border: 1.5px solid #D0D5DD;
        color: #344054;
        background-color: #FFFFFF;
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        border-color: #06B6D4;
        color: #06B6D4;
    }
    /* Botão "primário" (selecionado): preenchido e colorido */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #06B6D4;
        border: 1.5px solid #06B6D4;
    }
    /* Botão desabilitado (cifra ainda não implementada): contorno
       tracejado e opacidade reduzida, para não parecer clicável */
    div[data-testid="stButton"] > button:disabled {
        opacity: 0.55;
        border-style: dashed !important;
        cursor: not-allowed;
    }

    /* Cartão que envolve o conteúdo da cifra selecionada */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
        padding: 0.5rem 0.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Metadados de cada cifra — usados no cabeçalho do cartão
# ------------------------------------------------------------------
CIFRAS = {
    "Cifra de César": {
        "descricao": "Cifra de substituição simples: desloca cada letra do alfabeto em um número fixo de posições.",
        "app": cesar_app,
    },
    "Cifra de Vigenère": {
        "descricao": "Cifra de substituição polialfabética: usa uma palavra-chave para variar o deslocamento a cada letra.",
        "app": vigenere_app,
    },
    "Enigma": {
        "descricao": "Simulação do sistema de rotores usado na Segunda Guerra Mundial, com substituições que mudam a cada tecla pressionada.",
        "app": enigma_app,
    },
    "RSA": {
        "descricao": "Criptografia assimétrica baseada na dificuldade de fatorar números grandes, com par de chaves pública e privada.",
        "app": rsa_app,
    },
    "Hash": {
        "descricao": "Transforma uma entrada de qualquer tamanho em uma saída de tamanho fixo. Não é reversível — serve para verificar integridade.",
        "app": hash_app,
    },
}

# ------------------------------------------------------------------
# Cifras que ainda não têm um módulo implementado. Aparecem como
# botões desabilitados (cadeado), visíveis mas não clicáveis — é só
# adicionar o nome aqui; quando o módulo existir, basta "promovê-la"
# para o dicionário CIFRAS acima.
# ------------------------------------------------------------------
CIFRAS_EM_BREVE = ["ECC"]

# ------------------------------------------------------------------
# Estado da navegação (persiste entre reruns do Streamlit)
# ------------------------------------------------------------------
if "cifra_selecionada" not in st.session_state:
    st.session_state.cifra_selecionada = "Cifra de César"

# ------------------------------------------------------------------
# Título
# ------------------------------------------------------------------
st.title("🔐 Criptografia")
st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Layout: coluna estreita com os botões + coluna larga com o cartão
# ------------------------------------------------------------------
col_menu, col_conteudo = st.columns([1, 3], gap="large")

with col_menu:
    for nome_cifra in CIFRAS:
        selecionado = st.session_state.cifra_selecionada == nome_cifra
        if st.button(
            nome_cifra,
            key=f"botao_{nome_cifra}",
            type="primary" if selecionado else "secondary",
            use_container_width=True,
        ):
            st.session_state.cifra_selecionada = nome_cifra
            # Força um novo ciclo de execução imediatamente: sem isso, os
            # botões desenhados ANTES deste no laço ficariam com a cor
            # antiga, porque já teriam sido renderizados com o valor
            # anterior de session_state antes deste clique ser processado.
            st.rerun()

    # Cifras futuras: visíveis, com cadeado, desabilitadas
    if CIFRAS_EM_BREVE:
        st.markdown(
            "<div style='margin: 0.75rem 0 0.25rem 0; font-size: 0.8rem; "
            "color: #98A2B3;'>Em breve</div>",
            unsafe_allow_html=True,
        )
        for nome_futuro in CIFRAS_EM_BREVE:
            st.button(
                f"🔒 {nome_futuro}",
                key=f"bloqueado_{nome_futuro}",
                disabled=True,
                use_container_width=True,
                help=f"{nome_futuro} ainda não foi implementada nesta versão do app.",
            )

with col_conteudo:
    cifra_atual = CIFRAS[st.session_state.cifra_selecionada]

    with st.container(border=True):
        st.subheader(st.session_state.cifra_selecionada)
        st.caption(cifra_atual["descricao"])
        st.divider()

        # A partir daqui, quem desenha os campos reais de entrada e
        # saída é a própria função da cifra (cesar_app, vigenere_app...)
        cifra_atual["app"]()

st.sidebar.title("Navegação")
st.sidebar.info("Use os botões no topo da página para escolher a cifra.")
