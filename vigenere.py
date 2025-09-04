import streamlit as st

# O código para a cifra de Vigenère deve estar dentro de uma função.
# A função será importada pelo arquivo principal (app.py).
def app():
    """
    Exibe a página da Cifra de Vigenère.
    """
    st.title("🛡️ Cifra de Vigenère")
    st.write("Criptografe ou decriptografe uma mensagem usando a Cifra de Vigenère e uma chave de texto.")
    st.markdown("---")

    # Entrada do texto
    texto_original = st.text_area("Digite o texto:", height=150)
    
    # Entrada da chave
    chave = st.text_input("Digite a chave (uma palavra):").strip()

    # Processamento e exibição do resultado
    if texto_original and chave:
        def criptografar_vigenere(texto, chave):
            resultado = ""
            chave_repetida = (chave * (len(texto) // len(chave) + 1))[:len(texto)]
            chave_idx = 0

            for char in texto:
                if 'a' <= char <= 'z':
                    shift = ord(chave_repetida[chave_idx].lower()) - ord('a')
                    resultado += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                    chave_idx = (chave_idx + 1) % len(chave)
                elif 'A' <= char <= 'Z':
                    shift = ord(chave_repetida[chave_idx].upper()) - ord('A')
                    resultado += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                    chave_idx = (chave_idx + 1) % len(chave)
                else:
                    resultado += char
            return resultado

        texto_criptografado = criptografar_vigenere(texto_original, chave)
        
        st.subheader("Resultado")
        st.success(f"Texto Criptografado: **{texto_criptografado}**")
    elif not chave and texto_original:
        st.warning("Por favor, digite uma chave de texto.")
