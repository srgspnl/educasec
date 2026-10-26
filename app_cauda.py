"""
Busca Binária com Cauda Desordenada — versão Streamlit.

Executar:
    pip install streamlit pandas
    streamlit run app.py
"""
import math

import pandas as pd
import streamlit as st


# ----------------------------------------------------------------------
# Modelo (mesma lógica do notebook, sem prints: devolve mensagens)
# ----------------------------------------------------------------------
class SistemaCadastroClientes:
    """Parte ordenada (n elementos) + cauda desordenada (k elementos)."""

    def __init__(self, n_ordenados: int = 2**20):
        # Chaves pares 0, 2, 4, ... (ímpares ficam livres para testar chaves ausentes)
        self.parte_ordenada = list(range(0, n_ordenados * 2, 2))
        self.cauda_desordenada = []
        self._recalcular_limites()

    @property
    def n_ordenados(self) -> int:
        return len(self.parte_ordenada)

    @property
    def k(self) -> int:
        return len(self.cauda_desordenada)

    def _recalcular_limites(self) -> None:
        self.pior_caso_base = math.floor(math.log2(self.n_ordenados)) + 1
        self.limite_reordenacao = 2 * self.pior_caso_base

    def calcular_pior_caso_atual(self) -> int:
        return self.pior_caso_base + self.k

    def inserir_cliente(self, codigo: int, reordenar_automatico: bool = True) -> list[str]:
        msgs = []
        self.cauda_desordenada.append(codigo)
        pior = self.calcular_pior_caso_atual()
        msgs.append(f"[Inserção] código {codigo} | cauda k = {self.k:2d} | pior caso atual = {pior}")
        if reordenar_automatico and pior >= self.limite_reordenacao:
            msgs.append(f"⚠️ Limite atingido: pior caso = {pior} (dobro de {self.pior_caso_base}).")
            msgs += self.reordenar()
        return msgs

    def reordenar(self) -> list[str]:
        k = self.k
        msgs = [f"🔄 Reordenando: incorporando {k} elemento(s) da cauda..."]
        self.parte_ordenada = sorted(self.parte_ordenada + self.cauda_desordenada)
        self.cauda_desordenada = []
        self._recalcular_limites()
        msgs.append(f"✅ Concluído. Parte ordenada: {self.n_ordenados:,} registros | cauda: 0 | "
                    f"pior caso base: {self.pior_caso_base}")
        return msgs

    def consultar_cliente(self, codigo: int) -> dict:
        """Busca binária na parte ordenada; se falhar, busca linear na cauda."""
        iter_bin, iter_cauda = 0, 0
        local = None
        passos = []

        inicio, fim = 0, self.n_ordenados - 1
        while inicio <= fim:
            iter_bin += 1
            meio = (inicio + fim) // 2
            valor = self.parte_ordenada[meio]
            if valor == codigo:
                decisao = "achou"
            elif codigo > valor:
                decisao = "vai para a direita"
            else:
                decisao = "vai para a esquerda"
            passos.append({"iteração": iter_bin, "início": inicio, "fim": fim,
                           "meio": meio, "valor no meio": valor, "decisão": decisao})
            if valor == codigo:
                local = f"parte ordenada (posição {meio})"
                break
            elif codigo > valor:
                inicio = meio + 1
            else:
                fim = meio - 1

        if local is None:
            for pos, item in enumerate(self.cauda_desordenada):
                iter_cauda += 1
                if item == codigo:
                    local = f"cauda (posição {pos})"
                    break

        return {"encontrado": local is not None, "local": local,
                "iter_binaria": iter_bin, "iter_cauda": iter_cauda,
                "total": iter_bin + iter_cauda, "passos": passos}


# ----------------------------------------------------------------------
# Componentes de interface
# ----------------------------------------------------------------------
st.set_page_config(page_title="Busca Binária com Cauda", page_icon="📚", layout="wide")


@st.cache_resource(show_spinner=False)
def _base(n: int) -> tuple:
    """Lista base cacheada (evita recriar 1M de elementos a cada reset)."""
    return tuple(range(0, n * 2, 2))


def novo_sistema(n: int) -> SistemaCadastroClientes:
    s = SistemaCadastroClientes.__new__(SistemaCadastroClientes)
    s.parte_ordenada = list(_base(n))
    s.cauda_desordenada = []
    s._recalcular_limites()
    return s


def painel_metricas(s: SistemaCadastroClientes) -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Parte ordenada (n)", f"{s.n_ordenados:,}".replace(",", "."))
    c2.metric("Cauda (k)", s.k)
    c3.metric("Pior caso atual", s.calcular_pior_caso_atual(),
              delta=f"+{s.k} da cauda" if s.k else None, delta_color="inverse")
    c4.metric("Limite de reordenação", s.limite_reordenacao)
    frac = min(s.calcular_pior_caso_atual() / s.limite_reordenacao, 1.0)
    st.progress(frac, text=f"Pior caso: {s.calcular_pior_caso_atual()} de {s.limite_reordenacao} "
                           f"(base {s.pior_caso_base} + k {s.k})")


def mostrar_resultado(s: SistemaCadastroClientes, codigo: int, r: dict, titulo: str) -> None:
    st.markdown(f"**{titulo}**")
    if r["encontrado"]:
        st.success(f"Número **{codigo}** encontrado → {r['local']}")
    else:
        st.error(f"Número **{codigo}** não encontrado")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Iterações busca binária", r["iter_binaria"])
    c2.metric("Iterações na cauda", r["iter_cauda"])
    c3.metric("Total de buscas", r["total"])
    c4.metric("Pior caso teórico", s.calcular_pior_caso_atual())
    with st.expander("Ver os passos da busca binária"):
        st.dataframe(pd.DataFrame(r["passos"]), hide_index=True, width="stretch")


def resumo(r: dict) -> dict:
    return {k: r[k] for k in ("encontrado", "local", "iter_binaria", "iter_cauda", "total")}


# ----------------------------------------------------------------------
# Estado
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuração")
    expoente = st.slider("Tamanho da parte ordenada: n = 2^x", 4, 20, 20)
    n_inicial = 2 ** expoente
    st.caption(f"n = {n_inicial:,} registros (chaves pares 0, 2, 4, …)".replace(",", "."))
    auto = st.toggle("Reordenação automática", value=True,
                     help="Reordena quando o pior caso chega ao dobro do pior caso base.")
    if st.button("🔁 Reiniciar sistema", width="stretch") \
            or st.session_state.get("n_inicial") != n_inicial:
        st.session_state.sistema = novo_sistema(n_inicial)
        st.session_state.n_inicial = n_inicial
        st.session_state.log = []
        st.session_state.historico = []

sistema: SistemaCadastroClientes = st.session_state.sistema

st.title("📚 Busca Binária com Cauda Desordenada")
st.markdown(
    "Parte ordenada com busca binária + cauda desordenada com inserção O(1). "
    "Pior caso: $\\lfloor \\log_2 n \\rfloor + 1 + k$. "
    "A reordenação é disparada quando esse valor chega ao **dobro** do pior caso base."
)

aba_lab, aba_demo, aba_gatilho = st.tabs(
    ["🧪 Laboratório", "📊 Demonstração em 3 etapas", "⏱️ Gatilho automático"])

# ----------------------------------------------------------------------
# Aba 1 — Laboratório interativo
# ----------------------------------------------------------------------
with aba_lab:
    painel_metricas(sistema)
    col_ins, col_bus = st.columns(2)

    with col_ins:
        st.subheader("Inserir na cauda")
        texto = st.text_input("Códigos (separados por vírgula)", "900001, 900003, 1000001",
                              help="Use ímpares para que não existam na parte ordenada.")
        b1, b2 = st.columns(2)
        if b1.button("➕ Inserir", width="stretch"):
            try:
                codigos = [int(x.strip().replace("_", "").replace(".", ""))
                           for x in texto.split(",") if x.strip()]
            except ValueError:
                st.warning("Digite apenas números inteiros separados por vírgula.")
                codigos = []
            for c in codigos:
                st.session_state.log += sistema.inserir_cliente(c, reordenar_automatico=auto)
            st.rerun()
        if b2.button("🔄 Reordenar agora", width="stretch", disabled=sistema.k == 0):
            st.session_state.log += sistema.reordenar()
            st.rerun()
        if sistema.cauda_desordenada:
            st.caption("Cauda atual (ordem de inserção):")
            st.code(", ".join(map(str, sistema.cauda_desordenada)))

    with col_bus:
        st.subheader("Consultar")
        codigo = st.number_input("Número procurado", value=1_000_001, step=1)
        if st.button("🔍 Buscar", type="primary", width="stretch"):
            r = sistema.consultar_cliente(int(codigo))
            st.session_state.ultima = (int(codigo), r)
            st.session_state.historico.append(
                {"número": int(codigo), "n": sistema.n_ordenados, "k": sistema.k, **resumo(r),
                 "pior caso": sistema.calcular_pior_caso_atual()})
        if "ultima" in st.session_state:
            cod, r = st.session_state.ultima
            mostrar_resultado(sistema, cod, r, "Última consulta")

    if st.session_state.historico:
        st.subheader("Histórico de consultas")
        st.dataframe(pd.DataFrame(st.session_state.historico), hide_index=True,
                     width="stretch")

    if st.session_state.log:
        with st.expander("Registro de eventos", expanded=False):
            st.code("\n".join(st.session_state.log))

# ----------------------------------------------------------------------
# Aba 2 — Demonstração guiada (etapas do notebook)
# ----------------------------------------------------------------------
with aba_demo:
    st.markdown(
        "Reproduz o notebook em um sistema próprio (independente do laboratório): "
        "o mesmo número é buscado **antes da cauda**, **com a cauda** e **após a reordenação**."
    )
    numero_busca = st.number_input("Número de teste (ímpar)", value=1_000_001, step=2,
                                   key="num_demo")
    posicao = st.slider("Posição do número de teste na cauda", 1, 10, 8)

    if st.button("▶️ Executar demonstração", type="primary"):
        if numero_busca % 2 == 0:
            st.warning("Use um número ímpar: os pares já estão na parte ordenada.")
        else:
            demo = novo_sistema(n_inicial)
            log = []

            st.subheader("1. Lista só ordenada (sem cauda)")
            r1 = demo.consultar_cliente(int(numero_busca))
            mostrar_resultado(demo, int(numero_busca), r1, "Número de teste antes de ser inserido")

            st.subheader("2. Com a cauda (k = 10)")
            outros = [900_001 + 2 * i for i in range(9)]
            novos = outros[:posicao - 1] + [int(numero_busca)] + outros[posicao - 1:]
            for c in novos:
                log += demo.inserir_cliente(c, reordenar_automatico=False)
            st.code("\n".join(log))
            r2 = demo.consultar_cliente(int(numero_busca))
            mostrar_resultado(demo, int(numero_busca), r2, "Mesmo número com a cauda inserida")

            st.subheader("3. Após a reordenação")
            st.code("\n".join(demo.reordenar()))
            r3 = demo.consultar_cliente(int(numero_busca))
            mostrar_resultado(demo, int(numero_busca), r3, "Mesmo número após a reordenação")

            st.subheader("4. Resumo comparativo")
            tabela = pd.DataFrame([
                {"Situação": "1. Lista ordenada, sem cauda (ausente)", **resumo(r1)},
                {"Situação": "2. Com cauda (k = 10)", **resumo(r2)},
                {"Situação": "3. Após reordenação", **resumo(r3)},
            ])[["Situação", "iter_binaria", "iter_cauda", "total"]]
            tabela.columns = ["Situação", "Busca binária", "Cauda", "Total"]
            st.dataframe(tabela, hide_index=True, width="stretch")
            st.bar_chart(tabela.set_index("Situação")[["Busca binária", "Cauda"]], stack=True)

# ----------------------------------------------------------------------
# Aba 3 — Verificação do gatilho automático
# ----------------------------------------------------------------------
with aba_gatilho:
    base = math.floor(math.log2(n_inicial)) + 1
    st.markdown(
        f"Em um sistema novo (n = 2^{expoente}), inserimos elementos até o pior caso chegar a "
        f"**{2 * base}**. Na **{base}ª** inserção a reordenação dispara sozinha."
    )
    if st.button("▶️ Executar verificação", type="primary"):
        teste = novo_sistema(n_inicial)
        log, curva = [], []
        for i, c in enumerate(range(1001, 1001 + base), start=1):
            log += teste.inserir_cliente(c, reordenar_automatico=True)
            curva.append({"inserção": i, "pior caso": teste.pior_caso_base + i,
                          "limite": teste.limite_reordenacao})
        st.code("\n".join(log))
        st.line_chart(pd.DataFrame(curva).set_index("inserção"))
        ultimo = 1000 + base
        r = teste.consultar_cliente(ultimo)
        mostrar_resultado(teste, ultimo, r, "Busca do último código inserido, após a reordenação")
