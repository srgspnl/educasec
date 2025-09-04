import streamlit as st

# O código para a cifra de César deve estar dentro de uma função.
# A função será importada pelo arquivo principal (app.py).
def app():
    """
    Exibe a página da Cifra de César.
    """
    st.title("🛡️ Cifra de César")
    st.write("Criptografe ou decriptografe uma mensagem usando a Cifra de César, deslocando as letras do alfabeto.")
    st.markdown("---")

    # Entrada do texto
    texto_original = st.text_area("Digite o texto:", height=150)

    # Slider para escolher o deslocamento
    deslocamento = st.slider(
        "Escolha o deslocamento (chave):",
        min_value=1,
        max_value=25,
        value=3,
        step=1
    )

    # Processamento e exibição do resultado
    if texto_original:
        def criptografar_cesar(texto, chave):
            resultado = ""
            for char in texto:
                if 'a' <= char <= 'z':
                    resultado += chr((ord(char) - ord('a') + chave) % 26 + ord('a'))
                elif 'A' <= char <= 'Z':
                    resultado += chr((ord(char) - ord('A') + chave) % 26 + ord('A'))
                else:
                    resultado += char
            return resultado

        texto_criptografado = criptografar_cesar(texto_original, deslocamento)
        
        st.subheader("Resultado")
        st.success(f"Texto Criptografado: **{texto_criptografado}**")
