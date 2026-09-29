import pandas as pd
import streamlit as st

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Sistema Acadêmico",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

    /* Fundo geral */
    .stApp {
        background-color: #ffffff;
    }

    .main {
        background-color: #ffffff;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Título */
    .titulo {
    font-size: 38px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 4px;
    letter-spacing: -0.8px;
}

    .subtitulo {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    /* Cards principais */
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
    }

    .card-titulo {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 5px;
    }

    .card-valor {
        font-size: 30px;
        font-weight: 700;
        color: #1f2937;
    }

    /* Títulos das seções */
    .secao {
        font-size: 23px;
        font-weight: 650;
        color: #1f2937;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }

    /* Métricas */
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }

    [data-testid="stMetricValue"] {
        color: #1f2937 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #1f2937 !important;
    }
    /* Cores dos cards */
    .card-total {
        border-left: 5px solid #3b82f6;
    }

    .card-ativos {
        border-left: 5px solid #22c55e;
    }

    .card-trancados {
        border-left: 5px solid #f59e0b;
    }

    .card-evadidos {
        border-left: 5px solid #ef4444;
    }

    .card-media {
        border-left: 5px solid #8b5cf6;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# LEITURA DA PLANILHA
# ============================================================

arquivo = "Sistema Academico (1).xlsx"

df = pd.read_excel(
    arquivo,
    sheet_name="base_dados_academicos"
)

# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="titulo">🎓 Sistema Acadêmico</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Dashboard Executivo • Indicadores acadêmicos</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Filtros")

cursos = [
    "Todos"
] + sorted(
    df["curso"].dropna().unique().tolist()
)

curso_selecionado = st.sidebar.selectbox(
    "Curso",
    cursos
)

if curso_selecionado != "Todos":
    dados = df[df["curso"] == curso_selecionado].copy()
else:
    dados = df.copy()

st.sidebar.divider()

st.sidebar.info(
    "Use o filtro acima para visualizar os indicadores de um curso específico."
)

# ============================================================
# CÁLCULO DOS KPIs
# ============================================================

total_alunos = dados["id_aluno"].nunique()

alunos_ativos = dados.loc[
    dados["situacao_matricula"] == "Ativo",
    "id_aluno"
].nunique()

alunos_trancados = dados.loc[
    dados["situacao_matricula"] == "Trancado",
    "id_aluno"
].nunique()

alunos_evadidos = dados.loc[
    dados["situacao_matricula"] == "Evadido",
    "id_aluno"
].nunique()

media_final = dados["media_final"].mean()

frequencia_media = (
    dados["frequencia_pct"].mean() * 100
)

aprovados = (
    dados["situacao_disciplina"] == "Aprovado"
).sum()

reprovados = (
    dados["situacao_disciplina"] == "Reprovado"
).sum()

total_registros = len(dados)

taxa_aprovacao = (
    aprovados / total_registros * 100
)

taxa_reprovacao = (
    reprovados / total_registros * 100
)

# ============================================================
# CARDS PRINCIPAIS
# ============================================================

st.markdown(
    '<div class="secao">📊 Visão geral</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
        <div class="card card-total">
            <div class="card-titulo">👥 Total de alunos</div>
            <div class="card-valor">{total_alunos}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="card card-ativos">
            <div class="card-titulo">🟢 Alunos ativos</div>
            <div class="card-valor">{alunos_ativos}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="card card-trancados">
            <div class="card-titulo">⏸️ Trancados</div>
            <div class="card-valor">{alunos_trancados}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="card card-evadidos">
            <div class="card-titulo">🚪 Evadidos</div>
            <div class="card-valor">{alunos_evadidos}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class="card card-media">
            <div class="card-titulo">📚 Média final</div>
            <div class="card-valor">{media_final:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# SEGUNDA LINHA
# ============================================================

st.markdown(
    '<div class="secao">📈 Indicadores acadêmicos</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🔴 Taxa de evasão",
        f"{(alunos_evadidos / total_alunos) * 100:.1f}%"
    )

with col2:
    st.metric(
        "🟡 Taxa de trancamento",
        f"{(alunos_trancados / total_alunos) * 100:.1f}%"
    )

with col3:
    st.metric(
        "📅 Frequência média",
        f"{frequencia_media:.2f}%"
    )

with col4:
    st.metric(
        "✅ Aprovação",
        f"{taxa_aprovacao:.2f}%"
    )

with col5:
    st.metric(
        "❌ Reprovação",
        f"{taxa_reprovacao:.2f}%"
    )

# ============================================================
# GRÁFICO DE SITUAÇÃO
# ============================================================

st.markdown(
    '<div class="secao">🎯 Situação dos alunos</div>',
    unsafe_allow_html=True
)

situacao = (
    dados.groupby("situacao_matricula")["id_aluno"]
    .nunique()
)

st.bar_chart(
    situacao,
    width="stretch"
)

# ============================================================
# DESEMPENHO POR CURSO
# ============================================================

if curso_selecionado == "Todos":

    st.markdown(
        '<div class="secao">🏫 Desempenho por curso</div>',
        unsafe_allow_html=True
    )

    desempenho = (
    df.groupby("curso")
    .agg(
        Alunos=("id_aluno", "nunique"),
        Média=("media_final", "mean"),
        Frequência=("frequencia_pct", "mean"),
        Aprovação=("situacao_disciplina", lambda x: (x == "Aprovado").mean() * 100),
        Reprovação=("situacao_disciplina", lambda x: (x == "Reprovado").mean() * 100)
    )
)

    desempenho["Frequência"] *= 100

    desempenho = desempenho.round(2)

    st.dataframe(
        desempenho,
        width="stretch"
    )

# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Sistema Acadêmico • Desenvolvido em Python + Streamlit"
)

