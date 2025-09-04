import streamlit as st
import hashlib

def app():
    """
    Exibe a página de Criptografia de Hash.
    """
    st.title("🛡️ Funções de Hash")
    st.markdown("---")

    ## O que é uma Função de Hash?
    st.header("O que é uma Função de Hash?")
    st.write("""
    Uma **função de hash criptográfica** é como uma "impressora digital" para dados. Ela pega uma entrada (um texto, um arquivo, etc.) de qualquer tamanho e a transforma em uma string de caracteres de tamanho fixo, que é o **hash**.
    
    As principais características de uma função de hash são:
    1.  **É de mão única:** É extremamente fácil calcular o hash de uma mensagem, mas praticamente impossível reverter o processo e obter a mensagem original a partir do hash.
    2.  **Saída de tamanho fixo:** Independentemente do tamanho da entrada, a saída (o hash) terá sempre o mesmo tamanho. Por exemplo, o algoritmo SHA-256 sempre produz um hash de 256 bits (64 caracteres hexadecimais).
    3.  **Não-colisão:** É computacionalmente inviável encontrar duas entradas diferentes que gerem o mesmo hash.
    
    As funções de hash são amplamente utilizadas para verificar a integridade de dados e para armazenar senhas de forma segura.
    """)
    st.markdown("---")

    ## Gerar Hash
    st.header("Gerar Hash")
    
    # Entrada de texto
    texto_entrada = st.text_area(
        "Digite o texto para gerar o hash:",
        height=150
    )
    
    # Seleção do algoritmo de hash
    algoritmo_hash = st.selectbox(
        "Selecione o algoritmo de hash:",
        ("md5", "sha1", "sha256", "sha512")
    )
    
    if st.button("Gerar Hash"):
        if texto_entrada:
            # Codifica o texto para bytes (obrigatório para a biblioteca hashlib)
            texto_bytes = texto_entrada.encode('utf-8')
            
            # Cria o objeto de hash e atualiza-o com o texto
            hash_object = hashlib.new(algoritmo_hash)
            hash_object.update(texto_bytes)
            
            # Obtém o hash em formato hexadecimal
            hash_gerado = hash_object.hexdigest()
            
            st.subheader(f"Hash ({algoritmo_hash.upper()}) Gerado:")
            st.code(hash_gerado, language='text')
            
            st.info("Você pode mudar o texto ou o algoritmo para ver o hash ser alterado.")
        else:
            st.warning("Por favor, digite um texto para gerar o hash.")
