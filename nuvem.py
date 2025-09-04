# --- Dependências ---
# Este aplicativo requer as seguintes bibliotecas:
# streamlit
# wordcloud
# matplotlib
# spacy
# spacy.load("pt_core_news_sm") (modelo de idioma)
# pip install streamlit wordcloud matplotlib spacy
# python -m spacy download pt_core_news_sm

import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy
import re
import io

def app():
    """
    Função principal para a página de Nuvem de Palavras.
    """
    st.title("☁️ Gerador de Nuvem de Palavras")
    st.markdown("---")

    # Explicando o que é uma nuvem de palavras
    st.header("O que é uma nuvem de palavras?")
    st.write("""
    Uma nuvem de palavras é uma representação visual que destaca as palavras mais frequentes em um texto.
    Quanto maior a palavra, mais ela aparece no seu texto. Este aplicativo remove palavras
    comuns (como "o", "a", "de") e verbos para focar nas palavras-chave.
    """)
    st.markdown("---")

    # Carregar modelo spaCy
    try:
        nlp = st.session_state.get('nlp')
        if not nlp:
            st.info("Carregando o modelo de idioma. Isso pode levar alguns segundos...")
            nlp = spacy.load("pt_core_news_sm")
            st.session_state['nlp'] = nlp
            st.success("Modelo de idioma carregado com sucesso!")
    except OSError:
        st.warning("""
        O modelo de idioma 'pt_core_news_sm' não foi encontrado.
        Por favor, instale-o usando o seguinte comando no seu terminal:
        `python -m spacy download pt_core_news_sm`
        """)
        return

    # Entrada de texto do usuário
    texto_entrada = st.text_area(
        "Cole seu texto aqui (máximo 500 palavras):",
        height=300
    )

    # Processar o texto quando o botão for clicado
    if st.button("Gerar Nuvem de Palavras"):
        if not texto_entrada:
            st.warning("Por favor, cole um texto para gerar a nuvem.")
            return

        # Conta as palavras e verifica o limite
        words = texto_entrada.split()
        num_palavras = len(words)
        
        st.info(f"O seu texto tem **{num_palavras}** palavras.")
        
        if num_palavras > 500:
            st.warning("O seu texto excede o limite de 500 palavras. A nuvem será gerada com todas as palavras, mas considere um texto menor para melhores resultados.")

        # Normalizar texto (minúsculas e remoção de caracteres especiais)
        texto_normalizado = texto_entrada.lower()
        texto_normalizado = re.sub(r'[^\w\s]', '', texto_normalizado)

        # Processar com spaCy
        doc = nlp(texto_normalizado)

        # Filtrar palavras indesejadas
        palavras_filtradas = [
            token.text for token in doc
            if token.pos_ not in ["VERB", "CCONJ", "SCONJ", "ADP", "PRON"]
            and token.text not in nlp.Defaults.stop_words
            and len(token.text) > 2  # Remove palavras muito curtas
        ]

        # Juntar as palavras filtradas para a nuvem
        texto_filtrado = " ".join(palavras_filtradas)

        if not texto_filtrado.strip():
            st.warning("O texto não contém palavras-chave suficientes para gerar uma nuvem.")
            return

        # Gerar e exibir a nuvem de palavras
        with st.spinner("Gerando nuvem de palavras..."):
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                collocations=False
            ).generate(texto_filtrado)

            st.subheader("Sua Nuvem de Palavras")
            
            # Exibir a imagem usando Matplotlib
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
            # Botão para baixar a imagem
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button(
                label="Baixar Nuvem de Palavras",
                data=buf,
                file_name="nuvem_de_palavras.png",
                mime="image/png"
            )
