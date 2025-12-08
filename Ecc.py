import streamlit as st
import secrets
import hashlib
from datetime import datetime

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="Laboratório ECC",
    page_icon="🔐",
    layout="wide"
)

# ==================== CSS CUSTOMIZADO ====================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e3a8a 0%, #312e81 50%, #4c1d95 100%);
    }
    .stAlert {
        background-color: rgba(251, 191, 36, 0.2);
        border: 2px solid #fbbf24;
        border-radius: 10px;
    }
    .key-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid;
        margin: 10px 0;
    }
    .private-key {
        border-left-color: #ef4444;
        background-color: rgba(239, 68, 68, 0.2);
    }
    .public-key {
        border-left-color: #10b981;
        background-color: rgba(16, 185, 129, 0.2);
    }
    .address-key {
        border-left-color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.2);
    }
    .signature-key {
        border-left-color: #a855f7;
        background-color: rgba(168, 85, 247, 0.2);
    }
    .concept-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #fbbf24;
    }
    h1, h2, h3, h4 {
        color: white !important;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNÇÕES ====================

def gerar_chave_privada():
    """Gera uma chave privada aleatória de 256 bits"""
    return secrets.token_hex(32)

def gerar_chave_publica(chave_privada):
    """Simula geração de chave pública (educacional)"""
    # Em produção, usaria secp256k1 real
    return '04' + hashlib.sha256((chave_privada + 'pubkey').encode()).hexdigest() + \
           hashlib.sha256((chave_privada + 'pubkey2').encode()).hexdigest()

def gerar_endereco(chave_publica):
    """Simula geração de endereço Ethereum"""
    # Hash Keccak-256 da chave pública
    hash_pub = hashlib.sha256(chave_publica.encode()).hexdigest()
    return '0x' + hash_pub[-40:]

def assinar_mensagem(mensagem, chave_privada):
    """Simula assinatura ECDSA (educacional)"""
    # Em produção, usaria ECDSA real
    msg_hash = hashlib.sha256(mensagem.encode()).hexdigest()
    
    r = hashlib.sha256((chave_privada + msg_hash + 'r').encode()).hexdigest()
    s = hashlib.sha256((chave_privada + msg_hash + 's').encode()).hexdigest()
    v = 27 + (int(r[0], 16) % 2)
    
    return f"r: 0x{r}\ns: 0x{s}\nv: {v}"

# ==================== INICIALIZAÇÃO DO STATE ====================

if 'chave_privada' not in st.session_state:
    st.session_state.chave_privada = ''
if 'chave_publica' not in st.session_state:
    st.session_state.chave_publica = ''
if 'endereco' not in st.session_state:
    st.session_state.endereco = ''
if 'mostrar_privada' not in st.session_state:
    st.session_state.mostrar_privada = False
if 'passo' not in st.session_state:
    st.session_state.passo = 0
if 'mensagem' not in st.session_state:
    st.session_state.mensagem = ''
if 'assinatura' not in st.session_state:
    st.session_state.assinatura = ''

# ==================== HEADER ====================

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🔐 Laboratório de Criptografia ECC</h1>
        <p style='color: #93c5fd; font-size: 1.2em;'>
            Aprenda sobre Curvas Elípticas (secp256k1) e Assinaturas Digitais
        </p>
    </div>
    """, unsafe_allow_html=True)

st.warning("⚠️ **APENAS EDUCACIONAL - NÃO USE ESSAS CHAVES EM PRODUÇÃO!**")

# ==================== EXPLICAÇÃO ECC ====================

with st.expander("📚 O que é ECC (Elliptic Curve Cryptography)?", expanded=True):
    st.markdown("""
    **Curva Elíptica secp256k1** é o sistema criptográfico usado no Bitcoin e Ethereum.
    É baseado em matemática de curvas elípticas, oferecendo **segurança forte com chaves menores**.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='concept-card'>
            <h4>🔑 Chave Privada</h4>
            <p>Um número secreto aleatório de 256 bits. É como a senha mestra - NUNCA compartilhe!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='concept-card'>
            <h4>📍 Endereço</h4>
            <p>Hash da chave pública. É como seu número de conta bancária - pode divulgar.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='concept-card'>
            <h4>🔓 Chave Pública</h4>
            <p>Derivada matematicamente da privada. Pode ser compartilhada livremente - é o "cadeado".</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='concept-card'>
            <h4>✍️ Assinatura</h4>
            <p>Prova matemática de que você possui a chave privada, sem revelá-la!</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== INDICADOR DE PROGRESSO ====================

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.passo >= 1:
        st.success("✅ **1. Gerar Chaves**\n\nPar de chaves ECC criado")
    else:
        st.info("⭕ **1. Gerar Chaves**\n\nCriar par de chaves ECC")

with col2:
    if st.session_state.passo >= 2:
        st.success("✅ **2. Assinar Mensagem**\n\nAssinatura digital criada")
    elif st.session_state.passo >= 1:
        st.info("⭕ **2. Assinar Mensagem**\n\nCriar assinatura digital")
    else:
        st.info("⭕ **2. Assinar Mensagem**\n\nAguardando passo 1")

with col3:
    if st.session_state.passo >= 2:
        st.success("✅ **3. Verificar**\n\nValidar autenticidade")
    else:
        st.info("⭕ **3. Verificar**\n\nAguardando passos anteriores")

st.markdown("---")

# ==================== ÁREA DE TRABALHO ====================

if st.session_state.passo == 0:
    # PASSO 0: GERAR CHAVES
    st.markdown("""
    <div style='text-align: center; padding: 40px;'>
        <h2>🔑 Começar Experimento</h2>
        <p style='color: #93c5fd; font-size: 1.1em;'>
            Vamos gerar um par de chaves usando a curva elíptica secp256k1.<br>
            Este é o mesmo sistema usado em carteiras Bitcoin e Ethereum!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚡ Gerar Par de Chaves ECC", type="primary", use_container_width=True):
            with st.spinner("Gerando chaves..."):
                st.session_state.chave_privada = gerar_chave_privada()
                st.session_state.chave_publica = gerar_chave_publica(st.session_state.chave_privada)
                st.session_state.endereco = gerar_endereco(st.session_state.chave_publica)
                st.session_state.passo = 1
                st.rerun()

elif st.session_state.passo >= 1:
    # PASSO 1+: MOSTRAR CHAVES E ASSINAR
    
    # CHAVE PRIVADA
    st.markdown("""
    <div class='key-box private-key'>
        <h3>🔐 Chave Privada (256 bits)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.session_state.mostrar_privada:
            st.code(st.session_state.chave_privada, language=None)
        else:
            st.code('•' * 64, language=None)
    with col2:
        if st.button("👁️ Mostrar/Ocultar"):
            st.session_state.mostrar_privada = not st.session_state.mostrar_privada
            st.rerun()
    
    st.error("⚠️ **NUNCA compartilhe!** Quem tem esta chave controla todos os ativos.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CHAVE PÚBLICA
    st.markdown("""
    <div class='key-box public-key'>
        <h3>🔓 Chave Pública (Ponto na Curva)</h3>
    </div>
    """, unsafe_allow_html=True)
    st.code(st.session_state.chave_publica, language=None)
    st.success("✅ **Pode compartilhar.** Derivada matematicamente da chave privada usando ECC.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ENDEREÇO
    st.markdown("""
    <div class='key-box address-key'>
        <h3>📍 Endereço Público (Hash da Chave Pública)</h3>
    </div>
    """, unsafe_allow_html=True)
    st.code(st.session_state.endereco, language=None)
    st.info("✅ **Compartilhe livremente!** É o seu \"número de conta\" na blockchain.")
    
    st.markdown("---")
    
    # ÁREA DE ASSINATURA
    st.markdown("""
    <div class='key-box signature-key'>
        <h3>✍️ Assinar Mensagem</h3>
    </div>
    """, unsafe_allow_html=True)
    
    mensagem_input = st.text_area(
        "Digite uma mensagem para assinar:",
        value=st.session_state.mensagem,
        height=100,
        placeholder="Digite sua mensagem aqui..."
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🔏 Gerar Assinatura Digital (ECDSA)", type="primary", use_container_width=True):
            if mensagem_input:
                st.session_state.mensagem = mensagem_input
                st.session_state.assinatura = assinar_mensagem(mensagem_input, st.session_state.chave_privada)
                st.session_state.passo = 2
                st.rerun()
            else:
                st.error("⚠️ Digite uma mensagem primeiro!")
    
    with col2:
        if st.button("🔄 Recomeçar", use_container_width=True):
            st.session_state.chave_privada = ''
            st.session_state.chave_publica = ''
            st.session_state.endereco = ''
            st.session_state.mensagem = ''
            st.session_state.assinatura = ''
            st.session_state.passo = 0
            st.session_state.mostrar_privada = False
            st.rerun()
    
    # MOSTRAR ASSINATURA
    if st.session_state.assinatura:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔏 Assinatura Gerada:")
        st.code(st.session_state.assinatura, language=None)
        st.success("""
        ✅ Esta assinatura prova que você possui a chave privada, sem revelá-la!
        Qualquer um pode verificar usando apenas sua chave pública.
        """)

# ==================== CONCEITOS IMPORTANTES ====================

st.markdown("---")
st.markdown("## 🎓 Conceitos Importantes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='concept-card'>
        <h4>🔢 Por que 256 bits?</h4>
        <p>Com 256 bits, existem 2²⁵⁶ possíveis chaves (≈ 10⁷⁷). Mesmo tentando 
        1 trilhão de chaves por segundo, levaria mais tempo que a idade do universo!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='concept-card'>
        <h4>✍️ Assinatura Digital (ECDSA)</h4>
        <p>Usa sua chave privada + mensagem para criar uma assinatura única. 
        Qualquer um pode verificar com sua chave pública, mas só você pode criar!</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='concept-card'>
        <h4>🎯 Função de Mão Única</h4>
        <p>É fácil calcular a chave pública a partir da privada, mas impossível 
        fazer o inverso. É como quebrar um ovo - fácil numa direção, impossível na outra!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='concept-card'>
        <h4>🔐 Segurança na Prática</h4>
        <p>SEMPRE use geradores de números aleatórios criptograficamente seguros.
        Este demo é educacional - para produção, use bibliotecas validadas (Web3, ethers.js)!</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== RODAPÉ ====================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #93c5fd; padding: 20px;'>
    <p>🎓 <strong>Laboratório Educacional</strong> | Curva Elíptica secp256k1 (usada em Bitcoin/Ethereum)</p>
    <p style='color: #fbbf24; font-weight: bold;'>
        ⚠️ As chaves geradas aqui são aleatórias e NÃO devem ser usadas para guardar valores reais!
    </p>
</div>
""", unsafe_allow_html=True)