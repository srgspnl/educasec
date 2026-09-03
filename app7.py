import streamlit as st
import hashlib

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Corporativo · Criptografia",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS — replica o dashboard: sidebar azul-marinho, item ativo destacado,
# seção "EM BREVE" desabilitada, área principal cinza-clara com card branco
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        :root {
            --navy: #14274e;
            --navy-active: #2e5aac;
            --bg: #eef0f3;
            --text-muted: #6b7280;
        }

        .stApp { background-color: var(--bg); }

        section[data-testid="stSidebar"] {
            background-color: var(--navy);
            padding-top: 0;
        }
        section[data-testid="stSidebar"] > div {
            padding-top: 1.2rem;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #ffffff;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 0 1rem 1rem 1rem;
        }
        .sidebar-brand span.icon {
            color: #f5a524;
            font-size: 1.1rem;
        }

        div.stButton > button {
            width: 100%;
            text-align: left;
            background-color: transparent;
            border: none;
            border-radius: 6px;
            padding: 0.65rem 1rem;
            margin: 0.1rem 0.6rem;
            font-weight: 500;
            font-size: 0.92rem;
            color: #cfd8e3;
        }
        div.stButton > button:hover {
            background-color: rgba(255,255,255,0.08);
            color: #ffffff;
        }
        div.stButton > button:focus { box-shadow: none; }

        /* botão da página ativa */
        div.stButton.active > button {
            background-color: var(--navy-active) !important;
            color: #ffffff !important;
            font-weight: 600;
        }

        .em-breve-label {
            color: #7d8aa3;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            padding: 1.1rem 1.1rem 0.3rem 1.1rem;
        }
        .em-breve-item {
            color: #55617a;
            font-size: 0.92rem;
            padding: 0.55rem 1rem;
        }

        .top-eyebrow {
            color: var(--text-muted);
            font-size: 0.78rem;
            margin-bottom: 0.6rem;
        }

        .page-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #16233d;
            margin-bottom: 0.15rem;
        }
        .page-subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }
        hr.section-divider {
            border: none;
            border-top: 1px solid #dfe3e9;
            margin-bottom: 1.4rem;
        }

        .card {
            background-color: #ffffff;
            border-radius: 10px;
            border: 1px solid #e5e8ee;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
            padding: 1.6rem 1.8rem;
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #16233d;
            margin-bottom: 0.2rem;
        }
        .card-desc {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 1.1rem;
        }
        .field-label {
            font-weight: 600;
            font-size: 0.9rem;
            color: #1f2937;
            margin-bottom: 0.35rem;
        }

        textarea {
            border-radius: 8px !important;
            border: 1px solid #dfe3e9 !important;
            background-color: #f7f8fa !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Estado da navegação
# ---------------------------------------------------------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "Cifra de César"

opcoes = ["Cifra de César", "Cifra de Vigenère", "Enigma", "RSA", "Hash"]

# ---------------------------------------------------------------------------
# Menu lateral
# ---------------------------------------------------------------------------
st.sidebar.markdown(
    '<div class="sidebar-brand"><span class="icon">&#128274;</span> Criptografia</div>',
    unsafe_allow_html=True,
)

for opcao in opcoes:
    is_active = st.session_state.pagina == opcao
    # marca o wrapper do botão como ativo para o CSS acima
    wrapper_class = "active" if is_active else ""
    st.sidebar.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
    if st.sidebar.button(opcao, key=f"btn_{opcao}"):
        st.session_state.pagina = opcao
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown('<div class="em-breve-label">EM BREVE</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="em-breve-item">ECC</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Cabeçalho superior (breadcrumb estilo "06 · Dashboard Corporativo")
# ---------------------------------------------------------------------------
st.markdown('<div class="top-eyebrow">06 · Dashboard Corporativo</div>', unsafe_allow_html=True)

pagina = st.session_state.pagina

descricoes = {
    "Cifra de César": "Cifra de substituição simples: desloca cada letra do alfabeto em um número fixo de posições.",
    "Cifra de Vigenère": "Cifra de substituição polialfabética: usa uma palavra-chave para deslocar cada letra de forma variável.",
    "Enigma": "Simulação simplificada da máquina Enigma, usada para cifrar mensagens na Segunda Guerra Mundial.",
    "RSA": "Criptografia assimétrica baseada em um par de chaves pública e privada.",
    "Hash": "Funções de hash geram uma impressão digital única e irreversível para um texto.",
}

st.markdown(f'<div class="page-title">{pagina}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">{descricoes[pagina]}</div>', unsafe_allow_html=True)
st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Card principal por página
# ---------------------------------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f'<div class="card-title">{pagina}</div>', unsafe_allow_html=True)

if pagina == "Cifra de César":
    st.markdown(
        '<div class="card-desc">Criptografe ou decriptografe uma mensagem usando a Cifra de César, deslocando as letras do alfabeto.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="field-label">Digite o texto</div>', unsafe_allow_html=True)
    texto = st.text_area("", placeholder="Digite ou cole seu texto aqui...", label_visibility="collapsed", height=110)

    deslocamento = st.slider("Escolha o deslocamento (chave):", 1, 25, 3)

    modo = st.radio("Modo:", ["Cifrar", "Decifrar"], horizontal=True)

    def cesar(txt, k, decifrar=False):
        if decifrar:
            k = -k
        resultado = []
        for c in txt:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                resultado.append(chr((ord(c) - base + k) % 26 + base))
            else:
                resultado.append(c)
        return "".join(resultado)

    if st.button("Executar", key="exec_cesar"):
        st.success(cesar(texto, deslocamento, decifrar=(modo == "Decifrar")))

elif pagina == "Cifra de Vigenère":
    st.markdown(
        '<div class="card-desc">Criptografe ou decriptografe uma mensagem usando a Cifra de Vigenère e uma palavra-chave.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="field-label">Digite o texto</div>', unsafe_allow_html=True)
    texto = st.text_area("", placeholder="Digite ou cole seu texto aqui...", label_visibility="collapsed", height=110)

    chave = st.text_input("Chave (somente letras):", "chave")
    modo = st.radio("Modo:", ["Cifrar", "Decifrar"], horizontal=True)

    def vigenere(txt, chave, decifrar=False):
        chave = "".join([c for c in chave if c.isalpha()]).lower()
        if not chave:
            return txt
        resultado, idx = [], 0
        for c in txt:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                k = ord(chave[idx % len(chave)]) - ord('a')
                if decifrar:
                    k = -k
                resultado.append(chr((ord(c) - base + k) % 26 + base))
                idx += 1
            else:
                resultado.append(c)
        return "".join(resultado)

    if st.button("Executar", key="exec_vig"):
        st.success(vigenere(texto, chave, decifrar=(modo == "Decifrar")))

elif pagina == "Enigma":
    st.markdown(
        '<div class="card-desc">Funcionalidade em desenvolvimento — simulação da máquina Enigma.</div>',
        unsafe_allow_html=True,
    )
    st.info("Em breve.")

elif pagina == "RSA":
    st.markdown(
        '<div class="card-desc">Gere um par de chaves e cifre/decifre mensagens usando RSA.</div>',
        unsafe_allow_html=True,
    )
    st.info("Implemente aqui a geração de chaves e a lógica de cifrar/decifrar com RSA.")

elif pagina == "Hash":
    st.markdown(
        '<div class="card-desc">Gere o hash de um texto usando o algoritmo escolhido.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="field-label">Digite o texto</div>', unsafe_allow_html=True)
    texto = st.text_area("", placeholder="Digite ou cole seu texto aqui...", label_visibility="collapsed", height=110)
    algoritmo = st.selectbox("Algoritmo:", ["md5", "sha1", "sha256", "sha512"])
    if st.button("Gerar Hash", key="exec_hash"):
        h = hashlib.new(algoritmo)
        h.update(texto.encode("utf-8"))
        st.code(h.hexdigest())

st.markdown('</div>', unsafe_allow_html=True)
