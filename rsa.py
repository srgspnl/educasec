import streamlit as st
import base64

# Verificação de bibliotecas
try:
    from Crypto.Util import number
    from Crypto.PublicKey import RSA as CryptoRSA
    from Crypto.Cipher import PKCS1_OAEP
except ImportError:
    st.error("""
    ⚠️ A biblioteca `pycryptodome` não foi encontrada.
    Por favor, instale-a usando o seguinte comando no seu terminal:
    ```
    pip install pycryptodome
    ```
    """)
    st.stop()

# --- Funções de Ajuda ---
def generate_key_pair(bits):
    """
    Gera um par de chaves RSA (pública e privada) usando PyCryptodome.
    """
    key = CryptoRSA.generate(bits)
    
    public_key = key.publickey()
    
    # Extrai os componentes
    n = key.n
    e = key.e
    d = key.d
    
    return key, public_key, (e, n, d)

def key_to_pem(key, is_private=True):
    """
    Converte a chave para formato PEM.
    """
    if is_private:
        return key.export_key().decode('utf-8')
    else:
        return key.export_key().decode('utf-8')

def encrypt_message(public_key_pem, plaintext):
    """
    Criptografa uma mensagem usando PKCS1_OAEP (seguro).
    """
    public_key = CryptoRSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(public_key)
    
    # Divide a mensagem em blocos se necessário
    message_bytes = plaintext.encode('utf-8')
    max_chunk_size = (public_key.size_in_bytes() - 2 * 20 - 2)  # Para OAEP com SHA-1
    
    if len(message_bytes) > max_chunk_size:
        raise ValueError(f"Mensagem muito longa! Máximo: {max_chunk_size} bytes ({max_chunk_size} caracteres)")
    
    ciphertext = cipher.encrypt(message_bytes)
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt_message(private_key_pem, ciphertext_b64):
    """
    Descriptografa uma mensagem usando PKCS1_OAEP.
    """
    private_key = CryptoRSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key)
    
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext_bytes = cipher.decrypt(ciphertext)
    
    return plaintext_bytes.decode('utf-8')

# --- Interface do Streamlit ---
def app():
    st.set_page_config(page_title="RSA Criptografia", page_icon="🔐", layout="wide")
    
    st.title("🔐 Algoritmo RSA - Criptografia de Chave Pública")
    st.markdown("---")
    
    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["📚 O que é RSA?", "🔑 Gerar & Criptografar", "🔓 Descriptografar"])
    
    # ===== TAB 1: Explicação =====
    with tab1:
        st.header("O que é o RSA?")
        st.write("""
        O **RSA** (Rivest-Shamir-Adleman) é um dos algoritmos mais importantes de **criptografia assimétrica** 
        (chave pública). Foi publicado em 1977 e ainda é amplamente usado hoje.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔑 Como Funciona?")
            st.write("""
            1. **Geração de Chaves**: Dois números primos grandes (p e q) são multiplicados
            2. **Chave Pública**: Usada para criptografar (qualquer um pode ter)
            3. **Chave Privada**: Usada para descriptografar (só você tem)
            4. **Segurança**: Baseia-se na dificuldade de fatorar números grandes
            """)
            
        with col2:
            st.subheader("🎯 Aplicações")
            st.write("""
            - 🌐 HTTPS/SSL (segurança de websites)
            - 📧 Assinatura digital de emails
            - 💳 Transações bancárias online
            - 🔒 VPNs e conexões seguras
            """)
        
        st.markdown("---")
        st.subheader("📐 Entendendo os Parâmetros")
        
        st.markdown("""
        ### **e (Expoente Público)**
        - Parte da **chave pública**
        - Geralmente é **65537** (número primo, eficiente para cálculos)
        - Usado na **criptografia**: `c = m^e mod n`
        
        ### **n (Módulo)**
        - Parte de **ambas as chaves** (pública e privada)
        - É o produto de dois primos grandes: `n = p × q`
        - Seu tamanho determina a segurança (1024, 2048, 4096 bits)
        - Quanto maior o n, mais seguro (mas mais lento)
        
        ### **d (Expoente Privado)**
        - Parte da **chave privada** (deve ser mantido em SEGREDO!)
        - É o inverso multiplicativo de e: `d ≡ e^(-1) mod φ(n)`
        - Usado na **descriptografia**: `m = c^d mod n`
        - Se alguém descobrir d, pode descriptografar todas as mensagens!
        """)
        
        st.info("💡 **Lembre-se**: A segurança do RSA depende de manter a chave privada (d, n) em segredo absoluto!")
        
    # ===== TAB 2: Gerar & Criptografar =====
    with tab2:
        st.header("1️⃣ Gerar Par de Chaves")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            tamanho_bits = st.selectbox(
                "Tamanho da Chave (bits):",
                (1024, 2048, 4096),
                index=1,
                help="Maior = mais seguro, mas mais lento. 2048 bits é o padrão recomendado."
            )
        
        with col2:
            st.metric("Nível de Segurança", 
                     "Básico" if tamanho_bits == 1024 else "Recomendado" if tamanho_bits == 2048 else "Máximo")
        
        if st.button("🔄 Gerar Novo Par de Chaves", type="primary"):
            with st.spinner("Gerando chaves... Isso pode levar alguns segundos..."):
                private_key, public_key, components = generate_key_pair(tamanho_bits)
                e, n, d = components
                
                # Armazena no session_state
                st.session_state['private_key_obj'] = private_key
                st.session_state['public_key_obj'] = public_key
                st.session_state['private_key_pem'] = key_to_pem(private_key, True)
                st.session_state['public_key_pem'] = key_to_pem(public_key, False)
                st.session_state['components'] = (e, n, d)
                
                st.success("✅ Chaves geradas com sucesso!")
        
        if 'public_key_pem' in st.session_state:
            st.markdown("---")
            
            # Mostra componentes
            e, n, d = st.session_state['components']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Expoente Público (e)", "65537")
            with col2:
                st.metric("Tamanho do Módulo (n)", f"{n.bit_length()} bits")
            with col3:
                st.metric("Tamanho da Chave Privada (d)", f"{d.bit_length()} bits")
            
            # Expanders para mostrar valores completos
            with st.expander("🔍 Ver Componentes Matemáticos Completos"):
                st.code(f"e = {e}", language="python")
                st.code(f"n = {n}", language="python")
                st.code(f"d = {d}", language="python")
            
            # Mostra chaves em formato PEM
            st.subheader("🔑 Chaves em Formato PEM")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Chave Pública** (compartilhe com outros)")
                st.code(st.session_state['public_key_pem'], language="text")
                if st.button("📋 Copiar Chave Pública"):
                    st.toast("✅ Chave pública copiada!", icon="📋")
            
            with col2:
                st.write("**Chave Privada** (MANTENHA EM SEGREDO!)")
                st.code(st.session_state['private_key_pem'], language="text")
                if st.button("📋 Copiar Chave Privada"):
                    st.toast("✅ Chave privada copiada!", icon="📋")
            
            st.warning("⚠️ **IMPORTANTE**: A chave privada deve ser mantida em segredo absoluto! Não compartilhe com ninguém.")
            
            # Seção de Criptografia
            st.markdown("---")
            st.header("2️⃣ Criptografar Mensagem")
            
            max_chars = (n.bit_length() // 8) - 42
            
            texto_original = st.text_area(
                f"Digite a mensagem para criptografar (máx. ~{max_chars} caracteres):",
                height=100,
                help=f"Devido ao padding OAEP, mensagens são limitadas a aproximadamente {max_chars} caracteres"
            )
            
            if st.button("🔒 Criptografar Mensagem", type="primary"):
                if texto_original:
                    try:
                        ciphertext = encrypt_message(st.session_state['public_key_pem'], texto_original)
                        st.session_state['ciphertext'] = ciphertext
                        st.session_state['original_text'] = texto_original
                        
                        st.success("✅ Mensagem criptografada com sucesso!")
                        
                        st.subheader("📦 Mensagem Criptografada (Base64)")
                        st.code(ciphertext, language="text")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📋 Copiar Mensagem Criptografada"):
                                st.toast("✅ Mensagem criptografada copiada!", icon="📋")
                        with col2:
                            st.metric("Tamanho Original", f"{len(texto_original)} chars")
                        with col3:
                            st.metric("Tamanho Criptografado", f"{len(ciphertext)} chars")
                        
                    except ValueError as e:
                        st.error(f"❌ Erro: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Erro ao criptografar: {str(e)}")
                else:
                    st.warning("⚠️ Por favor, digite um texto para criptografar.")
            
            # Botão de descriptografar inline
            if 'ciphertext' in st.session_state:
                st.markdown("---")
                if st.button("🔓 Descriptografar Esta Mensagem"):
                    try:
                        decrypted = decrypt_message(
                            st.session_state['private_key_pem'], 
                            st.session_state['ciphertext']
                        )
                        
                        st.subheader("✅ Mensagem Descriptografada")
                        st.code(decrypted, language="text")
                        
                        if decrypted == st.session_state['original_text']:
                            st.success("✅ A mensagem foi descriptografada corretamente!")
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao descriptografar: {str(e)}")
        else:
            st.info("👆 Clique no botão acima para gerar um par de chaves primeiro.")
    
    # ===== TAB 3: Descriptografar =====
    with tab3:
        st.header("🔓 Descriptografar Mensagem")
        st.write("Use esta seção para descriptografar uma mensagem usando uma chave privada.")
        
        st.subheader("1️⃣ Cole a Chave Privada")
        private_key_input = st.text_area(
            "Chave Privada (formato PEM):",
            height=200,
            placeholder="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
        )
        
        st.subheader("2️⃣ Cole a Mensagem Criptografada")
        ciphertext_input = st.text_area(
            "Mensagem Criptografada (Base64):",
            height=100,
            placeholder="Cole aqui a mensagem criptografada em Base64..."
        )
        
        if st.button("🔓 Descriptografar", type="primary"):
            if not private_key_input:
                st.error("❌ Por favor, cole a chave privada.")
            elif not ciphertext_input:
                st.error("❌ Por favor, cole a mensagem criptografada.")
            else:
                try:
                    decrypted = decrypt_message(private_key_input, ciphertext_input)
                    
                    st.success("✅ Mensagem descriptografada com sucesso!")
                    st.subheader("📄 Texto Original")
                    st.code(decrypted, language="text")
                    
                    if st.button("📋 Copiar Texto Descriptografado"):
                        st.toast("✅ Texto descriptografado copiado!", icon="📋")
                    
                except ValueError as e:
                    st.error("❌ Chave privada inválida ou mensagem corrompida.")
                except Exception as e:
                    st.error(f"❌ Erro ao descriptografar: {str(e)}")
        
        st.markdown("---")
        st.info("""
        💡 **Dica**: Esta seção é útil quando você:
        - Recebe uma mensagem criptografada de outra pessoa
        - Quer descriptografar usando uma chave privada diferente
        - Está testando mensagens de outras fontes
        """)

if __name__ == "__main__":
    app()