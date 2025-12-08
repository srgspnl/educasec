# ecc.py
import streamlit as st
import hashlib
import json
from datetime import datetime

# Verificação de bibliotecas
try:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.backends import default_backend
    from cryptography.exceptions import InvalidSignature
except ImportError:
    st.error("""
    ⚠️ A biblioteca `cryptography` não foi encontrada.
    Por favor, instale-a usando:
    ```
    pip install cryptography
    ```
    """)
    st.stop()

# --- Funções Auxiliares ---

def generate_ecc_keypair(curve_name="SECP256R1"):
    """
    Gera um par de chaves ECC (pública e privada).
    """
    # Mapeia os nomes das curvas
    curves = {
        "SECP256R1": ec.SECP256R1(),
        "SECP384R1": ec.SECP384R1(),
        "SECP521R1": ec.SECP521R1()
    }
    
    curve = curves.get(curve_name, ec.SECP256R1())
    
    # Gera a chave privada
    private_key = ec.generate_private_key(curve, default_backend())
    
    # Obtém a chave pública
    public_key = private_key.public_key()
    
    return private_key, public_key

def serialize_private_key(private_key):
    """
    Serializa a chave privada para formato PEM.
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode('utf-8')

def serialize_public_key(public_key):
    """
    Serializa a chave pública para formato PEM.
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf-8')

def deserialize_private_key(pem_string):
    """
    Deserializa uma chave privada do formato PEM.
    """
    return serialization.load_pem_private_key(
        pem_string.encode('utf-8'),
        password=None,
        backend=default_backend()
    )

def deserialize_public_key(pem_string):
    """
    Deserializa uma chave pública do formato PEM.
    """
    return serialization.load_pem_public_key(
        pem_string.encode('utf-8'),
        backend=default_backend()
    )

def sign_message(private_key, message):
    """
    Assina uma mensagem usando a chave privada ECC.
    """
    signature = private_key.sign(
        message.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    return signature.hex()

def verify_signature(public_key, message, signature_hex):
    """
    Verifica a assinatura de uma mensagem usando a chave pública ECC.
    """
    try:
        signature = bytes.fromhex(signature_hex)
        public_key.verify(
            signature,
            message.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False

def hash_message(message):
    """
    Gera o hash SHA-256 de uma mensagem.
    """
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

# --- Interface Streamlit ---

def app():
    st.title("📈 Criptografia de Curvas Elípticas (ECC)")
    st.markdown("---")
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 O que é ECC?", 
        "🔑 Gerar Chaves", 
        "✍️ Assinar Documentos",
        "✅ Verificar Assinatura"
    ])
    
    # ===== TAB 1: Teoria =====
    with tab1:
        st.header("O que é ECC?")
        
        st.write("""
        A **Criptografia de Curvas Elípticas** (ECC - Elliptic Curve Cryptography) é um método moderno 
        de criptografia de chave pública baseado na matemática de curvas elípticas sobre campos finitos.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Por que ECC?")
            st.markdown("""
            - **Chaves menores**: 256 bits ECC ≈ 3072 bits RSA
            - **Mais rápido**: Operações mais eficientes
            - **Menos memória**: Ideal para dispositivos móveis
            - **Mesma segurança**: Com chaves muito menores
            """)
            
            st.subheader("📊 Comparação de Tamanhos")
            st.markdown("""
            | Algoritmo | Tamanho da Chave | Segurança |
            |-----------|------------------|-----------|
            | ECC-256   | 256 bits         | ⭐⭐⭐⭐⭐ |
            | RSA-3072  | 3072 bits        | ⭐⭐⭐⭐⭐ |
            | ECC-384   | 384 bits         | ⭐⭐⭐⭐⭐⭐ |
            | RSA-7680  | 7680 bits        | ⭐⭐⭐⭐⭐⭐ |
            """)
        
        with col2:
            st.subheader("🔐 Como Funciona?")
            st.markdown("""
            **1. Curva Elíptica**: Equação matemática especial  
            `y² = x³ + ax + b`
            
            **2. Ponto Base (G)**: Ponto conhecido na curva
            
            **3. Chave Privada (d)**: Número secreto aleatório
            
            **4. Chave Pública (Q)**: Ponto na curva  
            `Q = d × G`
            
            **5. Operações**: Multiplicação escalar na curva
            """)
            
            st.subheader("🌐 Aplicações")
            st.markdown("""
            - 🔒 **TLS/SSL**: Segurança em websites (HTTPS)
            - 💳 **Bitcoin/Blockchain**: Assinaturas digitais
            - 📱 **WhatsApp**: Criptografia end-to-end
            - 🔑 **SSH**: Autenticação segura
            - 📧 **PGP**: Emails criptografados
            """)
        
        st.markdown("---")
        
        st.subheader("📐 Curvas Elípticas Padrão")
        
        st.markdown("""
        Existem várias curvas padronizadas. As mais comuns são:
        
        - **SECP256R1** (P-256): Padrão NIST, 256 bits, amplamente usado
        - **SECP384R1** (P-384): Padrão NIST, 384 bits, segurança aumentada
        - **SECP521R1** (P-521): Padrão NIST, 521 bits, máxima segurança
        
        Nesta aplicação, usamos **SECP256R1** por ser o padrão mais comum e equilibrado.
        """)
        
        st.info("""
        💡 **Curiosidade**: A segurança do ECC se baseia na dificuldade do "Problema do Logaritmo 
        Discreto em Curvas Elípticas" (ECDLP), que é computacionalmente muito mais difícil que 
        a fatoração de números primos usada no RSA.
        """)
    
    # ===== TAB 2: Gerar Chaves =====
    with tab2:
        st.header("🔑 Geração de Chaves ECC")
        
        st.write("""
        Gere um par de chaves ECC para usar nas operações de assinatura e verificação.
        As chaves ECC são muito menores que RSA, mas oferecem o mesmo nível de segurança!
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            curve_option = st.selectbox(
                "Escolha a curva elíptica:",
                ["SECP256R1 (P-256) - Recomendado", "SECP384R1 (P-384)", "SECP521R1 (P-521)"],
                help="Curvas maiores oferecem mais segurança, mas são mais lentas"
            )
        
        with col2:
            curve_map = {
                "SECP256R1 (P-256) - Recomendado": "SECP256R1",
                "SECP384R1 (P-384)": "SECP384R1",
                "SECP521R1 (P-521)": "SECP521R1"
            }
            curve_name = curve_map[curve_option]
            
            security_level = {
                "SECP256R1": "128 bits",
                "SECP384R1": "192 bits",
                "SECP521R1": "256 bits"
            }
            
            st.metric("Segurança", security_level[curve_name])
        
        if st.button("🎲 Gerar Par de Chaves", type="primary"):
            with st.spinner("Gerando chaves ECC..."):
                private_key, public_key = generate_ecc_keypair(curve_name)
                
                private_pem = serialize_private_key(private_key)
                public_pem = serialize_public_key(public_key)
                
                # Armazena no session_state
                st.session_state['ecc_private_key'] = private_pem
                st.session_state['ecc_public_key'] = public_pem
                st.session_state['ecc_curve'] = curve_name
                
                st.success("✅ Chaves ECC geradas com sucesso!")
        
        if 'ecc_public_key' in st.session_state:
            st.markdown("---")
            
            # Informações sobre as chaves
            st.subheader("📊 Informações das Chaves")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Curva Elíptica", st.session_state['ecc_curve'])
            
            with col2:
                private_size = len(st.session_state['ecc_private_key'])
                st.metric("Tamanho Chave Privada", f"{private_size} bytes")
            
            with col3:
                public_size = len(st.session_state['ecc_public_key'])
                st.metric("Tamanho Chave Pública", f"{public_size} bytes")
            
            # Mostra as chaves
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🔒 Chave Privada (PEM)**")
                st.code(st.session_state['ecc_private_key'], language="text")
                if st.button("📋 Copiar Chave Privada"):
                    st.toast("✅ Chave privada copiada!", icon="📋")
            
            with col2:
                st.write("**🔓 Chave Pública (PEM)**")
                st.code(st.session_state['ecc_public_key'], language="text")
                if st.button("📋 Copiar Chave Pública"):
                    st.toast("✅ Chave pública copiada!", icon="📋")
            
            st.warning("⚠️ **IMPORTANTE**: Mantenha sua chave privada em segredo! Compartilhe apenas a chave pública.")
            
            st.info("""
            💡 **Como usar**:
            - Use a **chave privada** para assinar documentos (Tab "Assinar Documentos")
            - Compartilhe a **chave pública** com outros para que possam verificar suas assinaturas
            """)
    
    # ===== TAB 3: Assinar Documentos =====
    with tab3:
        st.header("✍️ Assinatura Digital de Documentos")
        
        st.write("""
        A assinatura digital garante **autenticidade** e **integridade** do documento.
        Funciona como uma "assinatura de caneta" digital que não pode ser falsificada!
        """)
        
        # Escolha do método
        st.subheader("1️⃣ Escolha o Método")
        
        metodo = st.radio(
            "Como deseja assinar?",
            ["🔑 Usar chave gerada nesta sessão", "📋 Colar minha chave privada"],
            help="Use a chave da sessão ou cole uma chave própria"
        )
        
        private_key_to_sign = None
        
        if metodo == "🔑 Usar chave gerada nesta sessão":
            if 'ecc_private_key' in st.session_state:
                st.success("✅ Usando chave privada da sessão atual")
                private_key_to_sign = st.session_state['ecc_private_key']
                
                with st.expander("🔍 Ver chave privada"):
                    st.code(st.session_state['ecc_private_key'], language="text")
            else:
                st.warning("⚠️ Nenhuma chave gerada nesta sessão. Vá para 'Gerar Chaves' ou cole sua chave abaixo.")
        
        else:
            private_key_input = st.text_area(
                "Cole sua Chave Privada (PEM):",
                height=200,
                placeholder="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
            )
            
            if private_key_input:
                private_key_to_sign = private_key_input
                st.success("✅ Chave privada fornecida")
        
        st.markdown("---")
        
        # Documento para assinar
        st.subheader("2️⃣ Documento a Assinar")
        
        tipo_entrada = st.radio(
            "Tipo de conteúdo:",
            ["📝 Texto", "📄 Upload de arquivo"],
            horizontal=True
        )
        
        documento = None
        nome_arquivo = None
        
        if tipo_entrada == "📝 Texto":
            documento = st.text_area(
                "Digite o texto do documento:",
                height=150,
                placeholder="Digite aqui o texto que deseja assinar digitalmente..."
            )
            nome_arquivo = "documento.txt"
        
        else:
            uploaded_file = st.file_uploader(
                "Faça upload do documento:",
                type=['txt', 'pdf', 'doc', 'docx', 'json'],
                help="Qualquer tipo de arquivo pode ser assinado"
            )
            
            if uploaded_file:
                documento = uploaded_file.read().decode('utf-8', errors='ignore')
                nome_arquivo = uploaded_file.name
                st.success(f"✅ Arquivo '{nome_arquivo}' carregado")
        
        # Botão de assinar
        if st.button("✍️ Assinar Documento", type="primary"):
            if not private_key_to_sign:
                st.error("❌ Por favor, forneça uma chave privada.")
            elif not documento:
                st.error("❌ Por favor, forneça um documento para assinar.")
            else:
                try:
                    # Deserializa a chave
                    private_key = deserialize_private_key(private_key_to_sign)
                    
                    # Gera o hash do documento
                    doc_hash = hash_message(documento)
                    
                    # Assina o documento
                    signature = sign_message(private_key, documento)
                    
                    # Armazena no session_state
                    st.session_state['signed_document'] = documento
                    st.session_state['signature'] = signature
                    st.session_state['doc_hash'] = doc_hash
                    st.session_state['doc_name'] = nome_arquivo
                    st.session_state['sign_timestamp'] = datetime.now().isoformat()
                    
                    st.success("✅ Documento assinado com sucesso!")
                    
                    st.markdown("---")
                    
                    # Mostra informações da assinatura
                    st.subheader("📦 Assinatura Digital Gerada")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Documento", nome_arquivo)
                        st.metric("Tamanho", f"{len(documento)} caracteres")
                    
                    with col2:
                        st.metric("Algoritmo", "ECDSA-SHA256")
                        st.metric("Tamanho Assinatura", f"{len(signature)} caracteres")
                    
                    st.write("**🔐 Hash do Documento (SHA-256)**")
                    st.code(doc_hash, language="text")
                    
                    st.write("**✍️ Assinatura Digital (Hex)**")
                    st.code(signature, language="text")
                    
                    if st.button("📋 Copiar Assinatura"):
                        st.toast("✅ Assinatura copiada!", icon="📋")
                    
                    # Pacote completo para compartilhar
                    st.markdown("---")
                    st.subheader("📤 Pacote Completo de Assinatura")
                    
                    pacote = {
                        "documento": documento,
                        "assinatura": signature,
                        "hash": doc_hash,
                        "arquivo": nome_arquivo,
                        "timestamp": st.session_state['sign_timestamp'],
                        "algoritmo": "ECDSA-SHA256",
                        "chave_publica": st.session_state.get('ecc_public_key', 'Não disponível')
                    }
                    
                    st.json(pacote)
                    
                    st.info("""
                    💡 **Para verificar a assinatura**:
                    1. Compartilhe este pacote (ou apenas a assinatura) com o destinatário
                    2. O destinatário precisa da sua chave pública
                    3. Use a aba "Verificar Assinatura" para validar
                    """)
                    
                except Exception as e:
                    st.error(f"❌ Erro ao assinar documento: {str(e)}")
    
    # ===== TAB 4: Verificar Assinatura =====
    with tab4:
        st.header("✅ Verificação de Assinatura Digital")
        
        st.write("""
        Verifique se um documento foi realmente assinado por quem diz ser o autor.
        A verificação garante autenticidade e integridade do documento.
        """)
        
        # Método de verificação
        st.subheader("1️⃣ Origem dos Dados")
        
        origem = st.radio(
            "De onde vêm os dados?",
            ["📦 Documento assinado nesta sessão", "📋 Colar dados manualmente"],
            help="Use dados da sessão atual ou dados externos"
        )
        
        documento_verificar = None
        assinatura_verificar = None
        chave_publica_verificar = None
        
        if origem == "📦 Documento assinado nesta sessão":
            if 'signed_document' in st.session_state:
                documento_verificar = st.session_state['signed_document']
                assinatura_verificar = st.session_state['signature']
                
                if 'ecc_public_key' in st.session_state:
                    chave_publica_verificar = st.session_state['ecc_public_key']
                
                st.success(f"✅ Usando documento assinado: {st.session_state.get('doc_name', 'documento.txt')}")
                
                with st.expander("🔍 Ver dados da assinatura"):
                    st.write("**Documento:**")
                    st.text(documento_verificar[:200] + "..." if len(documento_verificar) > 200 else documento_verificar)
                    st.write("**Assinatura:**")
                    st.code(assinatura_verificar[:100] + "...", language="text")
            else:
                st.warning("⚠️ Nenhum documento assinado nesta sessão. Use a opção de colar dados manualmente.")
        
        else:
            st.write("**📄 Documento Original**")
            documento_verificar = st.text_area(
                "Cole o texto do documento:",
                height=100,
                placeholder="Cole aqui o documento original que foi assinado..."
            )
            
            st.write("**✍️ Assinatura Digital**")
            assinatura_verificar = st.text_area(
                "Cole a assinatura (formato Hex):",
                height=80,
                placeholder="Cole aqui a assinatura em formato hexadecimal..."
            )
        
        st.markdown("---")
        
        # Chave pública
        st.subheader("2️⃣ Chave Pública do Signatário")
        
        metodo_chave = st.radio(
            "Fonte da chave pública:",
            ["🔑 Usar chave da sessão", "📋 Colar chave pública"],
            horizontal=True
        )
        
        if metodo_chave == "🔑 Usar chave da sessão":
            if 'ecc_public_key' in st.session_state:
                chave_publica_verificar = st.session_state['ecc_public_key']
                st.success("✅ Usando chave pública da sessão")
            else:
                st.warning("⚠️ Nenhuma chave na sessão. Cole a chave pública abaixo.")
        else:
            chave_input = st.text_area(
                "Cole a Chave Pública (PEM):",
                height=150,
                placeholder="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
            )
            
            if chave_input:
                chave_publica_verificar = chave_input
                st.success("✅ Chave pública fornecida")
        
        # Botão de verificar
        st.markdown("---")
        
        if st.button("🔍 Verificar Assinatura", type="primary"):
            if not documento_verificar:
                st.error("❌ Por favor, forneça o documento.")
            elif not assinatura_verificar:
                st.error("❌ Por favor, forneça a assinatura.")
            elif not chave_publica_verificar:
                st.error("❌ Por favor, forneça a chave pública.")
            else:
                try:
                    # Deserializa a chave pública
                    public_key = deserialize_public_key(chave_publica_verificar)
                    
                    # Verifica a assinatura
                    is_valid = verify_signature(public_key, documento_verificar, assinatura_verificar)
                    
                    # Calcula o hash para referência
                    doc_hash = hash_message(documento_verificar)
                    
                    st.markdown("---")
                    
                    if is_valid:
                        st.success("✅ **ASSINATURA VÁLIDA!**")
                        st.balloons()
                        
                        st.markdown("""
                        ### ✅ Verificação Bem-Sucedida
                        
                        A assinatura digital é **autêntica** e o documento está **íntegro**.
                        
                        **Isso significa que:**
                        - ✅ O documento foi realmente assinado pelo proprietário da chave privada
                        - ✅ O documento não foi alterado desde a assinatura
                        - ✅ A assinatura é matematicamente válida
                        """)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Status", "✅ VÁLIDA", delta="Autêntica")
                        
                        with col2:
                            st.metric("Integridade", "✅ PRESERVADA", delta="Não alterado")
                        
                        st.info(f"🔐 **Hash do Documento**: `{doc_hash}`")
                        
                    else:
                        st.error("❌ **ASSINATURA INVÁLIDA!**")
                        
                        st.markdown("""
                        ### ❌ Verificação Falhou
                        
                        A assinatura digital **não é válida**.
                        
                        **Possíveis razões:**
                        - ❌ O documento foi alterado após a assinatura
                        - ❌ A assinatura não corresponde ao documento
                        - ❌ A chave pública não corresponde à chave privada usada
                        - ❌ A assinatura está corrompida ou mal formatada
                        """)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Status", "❌ INVÁLIDA", delta="Não autêntica", delta_color="inverse")
                        
                        with col2:
                            st.metric("Integridade", "❌ COMPROMETIDA", delta="Possivelmente alterado", delta_color="inverse")
                        
                        st.warning("⚠️ **ATENÇÃO**: Não confie neste documento! A assinatura não pode ser verificada.")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao verificar assinatura: {str(e)}")
                    st.info("Verifique se a chave pública está no formato correto (PEM).")
        
        st.markdown("---")
        
        st.info("""
        💡 **Como funciona a verificação?**
        
        1. A chave pública descriptografa a assinatura
        2. O resultado é comparado com o hash do documento
        3. Se coincidirem, a assinatura é válida
        4. Qualquer alteração no documento invalida a assinatura
        """)

if __name__ == "__main__":
    app()