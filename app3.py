# app.py
import streamlit as st

# Importa as funções que contêm as lógicas de cada cifra
try:
    from cesar import app as cesar_app
    from vigenere import app as vigenere_app
    from enigma import app as enigma_app
    from rsa import app as rsa_app
    from hash import app as hash_app
    from ecc import app as ecc_app
except ImportError as e:
    st.error(f"""
    ⚠️ Erro ao importar módulos: {str(e)}
    
    Certifique-se de que os seguintes arquivos existem:
    - cesar.py
    - vigenere.py
    - enigma.py
    - rsa.py
    - hash.py
    - ecc.py
    """)
    st.stop()

# Configuração da página principal
st.set_page_config(
    page_title="🔐 App de Criptografia",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dicionário com informações sobre cada cifra
CIFRAS_INFO = {
    "Cifra de César": {
        "icone": "🔤",
        "descricao": "Cifra de substituição simples com deslocamento fixo",
        "nivel": "Básico"
    },
    "Cifra de Vigenère": {
        "icone": "🔡",
        "descricao": "Cifra polialfabética com chave de múltiplos caracteres",
        "nivel": "Intermediário"
    },
    "Enigma": {
        "icone": "⚙️",
        "descricao": "Máquina de criptografia usada na Segunda Guerra Mundial",
        "nivel": "Avançado"
    },
    "RSA": {
        "icone": "🔑",
        "descricao": "Criptografia assimétrica de chave pública",
        "nivel": "Avançado"
    },
    "ECC": {
        "icone": "📈",
        "descricao": "Criptografia de Curvas Elípticas (Elliptic Curve Cryptography)",
        "nivel": "Avançado"
    },
    "Hash": {
        "icone": "#️⃣",
        "descricao": "Funções hash criptográficas (MD5, SHA)",
        "nivel": "Intermediário"
    }
}

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-top: 0;
    }
    .stRadio > label {
        font-size: 1.1em;
        font-weight: 600;
        color: #333;
    }
    .info-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal da aplicação
st.markdown('<p class="main-title">🔐 Aplicação de Criptografia</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore diferentes algoritmos de criptografia</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Menu de navegação
st.sidebar.title("🧭 Navegação")
st.sidebar.markdown("Escolha um algoritmo de criptografia:")

# Opções do menu com ícones
opcoes = list(CIFRAS_INFO.keys())
opcoes_formatadas = [f"{CIFRAS_INFO[opt]['icone']} {opt}" for opt in opcoes]

opcao_selecionada = st.sidebar.radio(
    "",
    opcoes,
    format_func=lambda x: f"{CIFRAS_INFO[x]['icone']} {x}"
)

# Mostra informações sobre a cifra selecionada na sidebar
if opcao_selecionada:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Sobre esta cifra")
    
    info = CIFRAS_INFO[opcao_selecionada]
    
    st.sidebar.markdown(f"""
    **Descrição:**  
    {info['descricao']}
    
    **Nível de Complexidade:**  
    `{info['nivel']}`
    """)

# Rodapé da sidebar
st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica:** Use os algoritmos para aprender sobre criptografia de forma prática!")

# Mostra um card com informações antes de carregar a aplicação
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="info-box">
            <h2 style="text-align: center; margin-top: 0;">
                {CIFRAS_INFO[opcao_selecionada]['icone']} {opcao_selecionada}
            </h2>
            <p style="text-align: center; color: #666;">
                {CIFRAS_INFO[opcao_selecionada]['descricao']}
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Lógica para exibir a página correta
try:
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
except Exception as e:
    st.error(f"""
    ❌ **Erro ao carregar a aplicação {opcao_selecionada}:**
    
    ```
    {str(e)}
    ```
    
    Por favor, verifique se o módulo está implementado corretamente.
    """)
    
    # Mostra o traceback completo em um expander para debug
    with st.expander("🔍 Ver detalhes do erro (Debug)"):
        import traceback
        st.code(traceback.format_exc())

# Rodapé da aplicação
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>📚 <strong>Aplicação Educacional de Criptografia</strong></p>
    <p>Desenvolvido para fins didáticos • Explore, aprenda e experimente!</p>
</div>
""", unsafe_allow_html=True)
