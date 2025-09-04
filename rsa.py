import streamlit as st

# O Streamlit irá verificar a instalação desta biblioteca.
try:
    from Crypto.Util import number
except ImportError:
    st.warning("""
    A biblioteca `pycryptodome` não foi encontrada.
    Por favor, instale-a usando o seguinte comando no seu terminal:
    `pip install pycryptodome`
    """)
    st.stop()

# --- Funções de Ajuda ---
def generate_key_pair(bits):
    """
    Gera um par de chaves RSA (pública e privada).
    A chave pública é (e, n) e a privada é (d, n).
    """
    # Gera dois números primos grandes
    p = number.getPrime(bits // 2)
    q = number.getPrime(bits // 2)
    
    # Calcula o módulo n
    n = p * q
    
    # Calcula o totiente de Euler (phi)
    phi = (p - 1) * (q - 1)
    
    # Escolhe um expoente público e (geralmente um número primo pequeno)
    e = 65537
    
    # Calcula o expoente privado d, que é o inverso multiplicativo de e mod phi
    d = number.inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    """
    Criptografa uma mensagem usando a chave pública.
    """
    e, n = public_key
    
    # Converte o texto para um número (bytes)
    message_bytes = plaintext.encode('utf-8')
    message_num = int.from_bytes(message_bytes, 'big')
    
    # Cifra a mensagem: c = m^e mod n
    ciphertext_num = pow(message_num, e, n)
    
    return ciphertext_num

def decrypt(private_key, ciphertext):
    """
    Descriptografa uma mensagem usando a chave privada.
    """
    d, n = private_key
    
    # Descriptografa a mensagem: m = c^d mod n
    decrypted_num = pow(ciphertext, d, n)
    
    # Converte o número de volta para bytes e depois para texto
    decrypted_bytes = decrypted_num.to_bytes((decrypted_num.bit_length() + 7) // 8, 'big')
    
    # Remove o padding e decodifica para texto
    try:
        plaintext = decrypted_bytes.decode('utf-8')
        return plaintext
    except UnicodeDecodeError:
        return "Erro ao decodificar a mensagem. O texto original pode conter caracteres não UTF-8."

# --- Interface do Streamlit ---
def app():
    """
    Aplica-se a interface de usuário do Streamlit para o RSA.
    """
    st.title("🛡️ Algoritmo RSA")
    st.markdown("---")
    
    # O que é o RSA
    st.header("O que é o RSA?")
    st.write("""
    O RSA (Rivest-Shamir-Adleman) é um dos primeiros e mais populares algoritmos de **criptografia de chave pública**. Ele usa um par de chaves, uma pública e uma privada.
    
    * **Chave Pública:** É compartilhada com qualquer pessoa. É usada para **criptografar** dados.
    * **Chave Privada:** É mantida em segredo. É usada para **descriptografar** dados.
    
    A grande vantagem do RSA é que você pode enviar uma mensagem criptografada de forma segura para alguém usando a chave pública dela, e somente ela poderá decifrá-la usando sua chave privada.
    """)
    st.markdown("---")
    
    # Geração de Chaves
    st.header("1. Gerar Chaves")
    st.write("Clique no botão abaixo para gerar um novo par de chaves. O tamanho de bits determina a força da criptografia.")
    
    tamanho_bits = st.selectbox(
        "Tamanho da Chave (bits):",
        (1024, 2048, 4096),
        index=1
    )
    
    if st.button("Gerar Novo Par de Chaves"):
        with st.spinner("Gerando chaves... Isso pode levar alguns segundos..."):
            public_key, private_key = generate_key_pair(tamanho_bits)
            st.session_state['public_key'] = public_key
            st.session_state['private_key'] = private_key
            
            st.subheader("Chave Pública (e, n)")
            st.code(f"e: {public_key[0]}", language="python")
            st.code(f"n: {public_key[1]}", language="python")
            
            st.subheader("Chave Privada (d, n)")
            st.code(f"d: {private_key[0]}", language="python")
            st.code(f"n: {private_key[1]}", language="python")
            
            st.success("Chaves geradas com sucesso! Agora você pode criptografar uma mensagem.")
    
    st.markdown("---")
    
    # Criptografar e Descriptografar
    st.header("2. Criptografar e Descriptografar")
    if 'public_key' not in st.session_state:
        st.warning("Por favor, gere as chaves primeiro na seção acima.")
    else:
        public_key = st.session_state['public_key']
        private_key = st.session_state['private_key']
        
        texto_original = st.text_area(
            "Digite a mensagem para criptografar:",
            height=100
        )
        
        if st.button("Criptografar Mensagem"):
            if texto_original:
                try:
                    ciphertext_num = encrypt(public_key, texto_original)
                    st.session_state['ciphertext_num'] = ciphertext_num
                    
                    st.subheader("Mensagem Criptografada")
                    st.code(f"{ciphertext_num}", language="python")
                    
                    st.success("Mensagem criptografada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao criptografar: {e}")
            else:
                st.warning("Por favor, digite um texto para criptografar.")

        if 'ciphertext_num' in st.session_state:
            st.markdown("---")
            st.subheader("Descriptografar Mensagem")
            
            if st.button("Descriptografar"):
                ciphertext_num = st.session_state['ciphertext_num']
                try:
                    texto_descriptografado = decrypt(private_key, ciphertext_num)
                    
                    st.subheader("Mensagem Descriptografada")
                    st.code(texto_descriptografado, language="python")
                    
                    st.info("A mensagem foi descriptografada usando a chave privada.")
                except Exception as e:
                    st.error(f"Erro ao descriptografar: {e}")
