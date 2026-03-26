import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EstudaEasy DW", layout="wide")
st.title("📊 Dashboard - EstudaEasy (Data Warehouse)")

# Upload do CSV
uploaded_file = st.file_uploader("📁 Faça upload do CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(
        uploaded_file,
        header=None,
        names=["name", "pergunta", "resposta", "data", "hora"],
        on_bad_lines="skip"
    )

    df = df[df["name"].notna() & (df["name"].str.strip() != "")]
    df["name"] = df["name"].fillna("Desconhecido")
    df["data"] = df["data"].fillna("Sem data")
    df["hora"] = df["hora"].fillna("Sem hora").astype(str)

    st.success(f"Arquivo carregado! {len(df)} registros válidos.")

    st.subheader("🔍 Pré-visualização dos dados")
    st.dataframe(df.head())

   
    st.sidebar.header("🎯 Filtros")

    if "name" in df.columns:
        usuarios = st.sidebar.multiselect(
            "Usuário",
            df["name"].unique(),
            default=df["name"].unique()
        )
        df = df[df["name"].isin(usuarios)]

    if "data" in df.columns:
        datas = st.sidebar.multiselect(
            "Data",
            sorted(df["data"].unique()),
            default=sorted(df["data"].unique())
        )
        df = df[df["data"].isin(datas)]

    if "hora" in df.columns:
        horas = st.sidebar.multiselect(
            "Hora",
            sorted(df["hora"].unique()),
            default=sorted(df["hora"].unique())
        )
        df = df[df["hora"].isin(horas)]

    st.subheader("📌 Indicadores")

    col1, col2, col3 = st.columns(3)
    col1.metric("💬 Total de Perguntas", len(df))
    col2.metric("👤 Usuários Ativos", df["name"].nunique())
    col3.metric("📅 Dias com Atividade", df["data"].nunique())
    

    # Top 10 perguntas
    st.subheader("📊 Perguntas mais frequentes")
    top_perguntas = df["pergunta"].value_counts().reset_index()
    top_perguntas.columns = ["pergunta", "total"]
    fig1 = px.bar(top_perguntas.head(10), x="pergunta", y="total",
                  title="Top 10 perguntas")
    st.plotly_chart(fig1, use_container_width=True)

    # Uso por usuário
    st.subheader("👤 Perguntas por Usuário")
    uso_usuario = df["name"].value_counts().reset_index()
    uso_usuario.columns = ["name", "total"]
    fig2 = px.bar(uso_usuario, x="name", y="total",
                  title="Total de perguntas por usuário")
    st.plotly_chart(fig2, use_container_width=True)

    # 🍕 Pizza por usuário
    st.subheader("🍕 Distribuição por Usuário")

    uso_usuario_top = uso_usuario.head(5)

    fig3 = px.pie(
        uso_usuario_top,
        names="name",
        values="total",
        title="Participação de cada usuário",
        hole=0.5  # 👈 donut
    )

    fig3.update_layout(
        height=400, 
        margin=dict(t=40, b=40, l=40, r=40)
    )

    fig3.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Evolução por dia
    if "data" in df.columns:
        st.subheader("📅 Evolução por Dia")
        uso_dia = df.groupby("data").size().reset_index(name="total")
        fig4 = px.line(uso_dia, x="data", y="total", markers=True,
                       title="Perguntas por dia")
        st.plotly_chart(fig4, use_container_width=True)


else:
    st.info("Faça upload do CSV para visualizar o dashboard.")

