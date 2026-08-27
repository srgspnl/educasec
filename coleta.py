import streamlit as st

# Configuração da página para simular tela mobile
st.set_page_config(page_title="Recicla+", page_icon="🌱", layout="centered")

# Estilização CSS customizada para manter o tema Dark & Lime do protótipo HTML
st.markdown("""
<style>
    /* Estilo global e tema Dark */
    .stApp {
        background-color: #0a0b0c;
        color: #f4f5f2;
    }
    
    /* Alerta Superior */
    .alert-bar {
        background-color: #fdfdfb;
        color: #1c1c1c;
        text-align: center;
        padding: 8px;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    /* Cards */
    .custom-card {
        background-color: #1e2124;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 15px;
    }

    /* Cores de destaque */
    .lime-text { color: #c7e63a; }
    .sub-text { color: #7d8280; font-size: 0.85em; }
    .val-text { font-size: 2rem; font-weight: bold; color: #f4f5f2; }
    
    /* Ajustes nos botões nativos do Streamlit */
    div.stButton > button {
        width: 100%;
        background-color: #26292d;
        color: #c7e63a;
        border: none;
        border-radius: 10px;
    }
    div.stButton > button:hover {
        background-color: #c7e63a;
        color: #12140f;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- BARRA DE ALERTA -----------------
st.markdown('<div class="alert-bar">⚠️ 🔥 🔥 🔥</div>', unsafe_allow_html=True)

# ----------------- CABEÇALHO / PERFIL -----------------
col_prof, col_btns = st.columns([2, 1])

with col_prof:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: #22251f; padding: 10px; border-radius: 50%;">💳</div>
            <div>
                <div class="sub-text">Nível 1 · Semente</div>
                <div style="font-weight: bold; font-size: 1.2rem;">Sergio</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_btns:
    c1, c2, c3 = st.columns(3)
    if c1.button("👛", key="hdr_wallet"):
        st.info("botão clicado")
    if c2.button("🔔", key="hdr_notif"):
        st.info("botão clicado")
    if c3.button("☰", key="hdr_menu"):
        st.info("botão clicado")

st.divider()

# ----------------- BARRA DE PROGRESSO -----------------
st.markdown('<div class="sub-text">Progresso do Nível</div>', unsafe_allow_html=True)
col_p1, col_p2, col_p3 = st.columns([1, 4, 1])

with col_p1:
    st.write("🌱 → 🌿")
with col_p2:
    st.progress(0.0) # 0% de progresso
with col_p3:
    if st.button("❓", key="btn_help"):
        st.info("botão clicado")

st.caption("0/12 pontos")

# ----------------- CARD TRICOINS -----------------
st.markdown("""
<div class="custom-card">
    <div class="sub-text">Tricoins</div>
    <div class="val-text">10</div>
</div>
""", unsafe_allow_html=True)

col_tc1, col_tc2 = st.columns(2)
if col_tc1.button("🤍 Favoritar", key="btn_fav"):
    st.info("botão clicado")
if col_tc2.button("🔄 Trocar", key="btn_swap"):
    st.info("botão clicado")

# ----------------- LIMITE DIÁRIO -----------------
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.subheader("Limite Diário Restante")

l1, l2, l3 = st.columns(3)
with l1:
    st.markdown("**0 / 10**")
    st.caption("Retorna Machine")
with l2:
    st.markdown("**0 / 10**")
    st.caption("Recicla Pharma")
with l3:
    st.markdown("**0 / 3**")
    st.caption("Deixaki")
st.markdown('</div>', unsafe_allow_html=True)

# ----------------- VEJA COMO RECICLAR -----------------
st.subheader("Veja Como Reciclar")
m1, m2, m3, m4 = st.columns(4)

if m1.button("🤖\nRetorna Machine"):
    st.info("botão clicado")
if m2.button("💊\nRecicla Pharma"):
    st.info("botão clicado")
if m3.button("📦\nDeixaki"):
    st.info("botão clicado")
if m4.button("🚉\nRecicla Station"):
    st.info("botão clicado")

# ----------------- CLUBE DE VANTAGENS -----------------
st.markdown("---")
if st.button("🎁 **Clube de Vantagens** — Descubra muito mais benefícios disponíveis para troca! ➔"):
    st.info("botão clicado")

# ----------------- ONDE RECICLAR -----------------
st.subheader("Onde reciclar?")
st.caption("Encontre agora a máquina de reciclagem mais perto de você.")

if st.button("📍 Localizar Máquina Próxima", key="btn_map"):
    st.info("botão clicado")

# ----------------- NAVEGAÇÃO INFERIOR -----------------
st.divider()
nav1, nav2, nav3, nav4, nav5 = st.columns(5)

if nav1.button("🏠\nHome"):
    st.info("botão clicado")
if nav2.button("📄\nExtrato"):
    st.info("botão clicado")
if nav3.button("🔳\nVIVO"):
    st.info("botão clicado")
if nav4.button("🌱\nEco Pontos"):
    st.info("botão clicado")
if nav5.button("👤\nPerfil"):
    st.info("botão clicado")