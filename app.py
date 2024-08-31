import streamlit as st
import pandas as pd
import plotly.express as px

# Dados iniciais (você pode substituir por um DataFrame real)
df = pd.DataFrame({
    "Data": pd.to_datetime(["2024-08-01", "2024-08-02", "2024-08-03"]),
    "Categoria": ["Alimentação", "Transporte", "Entretenimento"],
    "Valor": [820, 500, 850],
    "Tipo": ["Despesa", "Despesa", "Despesa"]
})

# Converte a coluna 'Data' para datetime
df['Data'] = pd.to_datetime(df['Data'])

# Título do app
st.title("Dashboard de Controle Financeiro Pessoal")

# Formulário para adicionar novas despesas
with st.form("Nova despesa"):
    categoria = st.selectbox("Categoria", options=["Alimentação", "Transporte", "Entretenimento", "Salário"])
    valor = st.number_input("Valor", min_value=0.0, step=0.01)
    tipo = st.selectbox("Tipo", options=["Despesa", "Receita"])
    data = st.date_input("Data")
    adicionar = st.form_submit_button("Adicionar")

    if adicionar:
        novo_dado = {"Data": pd.to_datetime(data), "Categoria": categoria, "Valor": valor, "Tipo": tipo}
        df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
        st.success("Dado adicionado com sucesso!")

# Filtros laterais
categoria_selecionada = st.sidebar.multiselect("Categoria", options=df['Categoria'].unique())
tipo_selecionado = st.sidebar.selectbox("Tipo", options=["Todos", "Despesa", "Receita"])
data_inicio = st.sidebar.date_input("Data Início", df['Data'].min().date())  # Convertendo para date
data_fim = st.sidebar.date_input("Data Fim", df['Data'].max().date())  # Convertendo para date

# Aplicação dos filtros
if categoria_selecionada:
    df = df[df['Categoria'].isin(categoria_selecionada)]
if tipo_selecionado != "Todos":
    df = df[df['Tipo'] == tipo_selecionado]
df = df[(df['Data'] >= pd.to_datetime(data_inicio)) & (df['Data'] <= pd.to_datetime(data_fim))]

# Mostrar dados filtrados
st.dataframe(df)

# Gráfico de barras interativo
st.subheader("Gráfico de colunas")
fig_bar = px.bar(df, x="Categoria", y="Valor", color="Tipo", barmode="group", title="Despesas e Receitas por Categoria")
st.plotly_chart(fig_bar)

# Gráfico de pizza interativo
st.subheader("gráfico de setores")
fig_pie = px.pie(df, values="Valor", names="Categoria", title="Distribuição de Despesas e Receitas por Categoria")
st.plotly_chart(fig_pie)

