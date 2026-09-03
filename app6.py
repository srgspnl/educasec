import streamlit as st

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="App de Cifras",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS customizado para deixar o menu lateral parecido com o wireframe
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            background-color: #f4f4f4;
            border-right: 2px solid #1a1a1a;
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }
        div.stButton > button {
            width: 100%;
            text-align: left;
            background-color: transparent;
            border: none;
            border-bottom: 1px solid #cccccc;
            border-radius: 0px;
            padding: 0.9rem 0.6rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            color: #1a1a1a;
        }
        div.stButton > button:hover {
            background-color: #e0e0e0;
            color: #000000;
        }
        div.stButton > button:focus {
            box-shadow: none;
        }
        .menu-title {
            font-weight: 800;
            letter-spacing: 0.1em;
            font-size: 0.85rem;
            color: #555555;
            margin: 0.6rem 0 0.4rem 0.6rem;
        }
        .page-title {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            border-bottom: 3px solid #1a1a1a;
            padding-bottom: 0.4rem;
            margin-bottom: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Estado da navegação
# ---------------------------------------------------------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "SOBRE"

opcoes = ["SOBRE", "CÉSAR", "VIGENÈRE", "RSA", "HASH"]

# ---------------------------------------------------------------------------
# Menu lateral
# ---------------------------------------------------------------------------
st.sidebar.markdown('<div class="menu-title">[ MENU LATERAL ]</div>', unsafe_allow_html=True)

for opcao in opcoes:
    if st.sidebar.button(opcao, key=f"btn_{opcao}"):
        st.session_state.pagina = opcao

st.sidebar.markdown("---")
st.sidebar.info("Escolha uma cifra no menu acima para começar.")

# ---------------------------------------------------------------------------
# Componente visual: forma de "gravata/ampulheta" com texto central
# (reproduz o desenho do wireframe: EXIBE CIFRA no centro)
# ---------------------------------------------------------------------------
def desenho_ampulheta(texto_central: str = "EXIBE<br/>CIFRA"):
    svg = f"""
    <div style="width:100%; display:flex; justify-content:center; margin-top:1rem;">
        <svg viewBox="0 0 800 420" width="100%" height="420" preserveAspectRatio="xMidYMid meet">
            <polygon points="0,0 800,0 400,210 800,420 0,420 400,210"
                     fill="none" stroke="#1a1a1a" stroke-width="2"/>
            <foreignObject x="280" y="160" width="240" height="100">
                <div xmlns="http://www.w3.org/1999/xhtml"
                     style="width:100%; height:100%; display:flex; align-items:center;
                            justify-content:center; text-align:center; font-family:sans-serif;
                            font-weight:800; letter-spacing:0.08em; font-size:22px; color:#1a1a1a;
                            line-height:1.3;">
                    {texto_central}
                </div>
            </foreignObject>
        </svg>
    </div>
    """
    st.markdown(svg, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Conteúdo principal por página
# ---------------------------------------------------------------------------
pagina = st.session_state.pagina

if pagina == "SOBRE":
    st.markdown('<p class="page-title">CIFRA jogue...</p>', unsafe_allow_html=True)
    desenho_ampulheta("EXIBE<br/>CIFRA")
    st.write("")
    st.markdown(
        """
        Bem-vindo(a) ao **App de Cifras**! Use o menu lateral para explorar cada técnica de
        criptografia: **César**, **Vigenère**, **RSA** e **Hash**.
        """
    )

elif pagina == "CÉSAR":
    st.markdown('<p class="page-title">CIFRA DE CÉSAR</p>', unsafe_allow_html=True)
    st.write("")
    modo = st.radio("Modo:", ["Cifrar", "Decifrar"], horizontal=True)
    texto = st.text_area("Texto:")
    deslocamento = st.slider("Deslocamento (chave):", 1, 25, 3)

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

    if st.button("Executar"):
        saida = cesar(texto, deslocamento, decifrar=(modo == "Decifrar"))
        st.success(saida)

elif pagina == "VIGENÈRE":
    st.markdown('<p class="page-title">CIFRA DE VIGENÈRE</p>', unsafe_allow_html=True)
    st.write("")
    modo = st.radio("Modo:", ["Cifrar", "Decifrar"], horizontal=True)
    texto = st.text_area("Texto:")
    chave = st.text_input("Chave (somente letras):", "chave")

    def vigenere(txt, chave, decifrar=False):
        chave = "".join([c for c in chave if c.isalpha()]).lower()
        if not chave:
            return txt
        resultado = []
        idx = 0
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

    if st.button("Executar"):
        saida = vigenere(texto, chave, decifrar=(modo == "Decifrar"))
        st.success(saida)

elif pagina == "RSA":
    st.markdown('<p class="page-title">CIFRA RSA</p>', unsafe_allow_html=True)
    st.write("")
    st.info("Implemente aqui a geração de chaves e a lógica de cifrar/decifrar com RSA.")

elif pagina == "HASH":
    st.markdown('<p class="page-title">FUNÇÕES HASH</p>', unsafe_allow_html=True)
    st.write("")
    import hashlib
    texto = st.text_area("Texto:")
    algoritmo = st.selectbox("Algoritmo:", ["md5", "sha1", "sha256", "sha512"])
    if st.button("Gerar Hash"):
        h = hashlib.new(algoritmo)
        h.update(texto.encode("utf-8"))
        st.code(h.hexdigest())
