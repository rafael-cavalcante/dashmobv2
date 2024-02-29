import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Divm",
    page_icon="📊",
    layout="wide")

df = pd.read_csv("dados_violencia_mulheres_ses_2023.csv", delimiter=";")

#Variáveis 
meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
         7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

#Gráfico 01
df["DT_NOTIFIC"] = pd.to_datetime(df["DT_NOTIFIC"], format="%d/%m/%Y")

df = df.sort_values("DT_NOTIFIC")

df["Mes_Numero"] = df["DT_NOTIFIC"].dt.month

quantidade_por_mes = df.groupby("Mes_Numero").size().reset_index(name="Quantidade")

quantidade_por_mes["Mes"] = quantidade_por_mes["Mes_Numero"].map(meses)

quantidade_por_mes = quantidade_por_mes.drop("Mes_Numero", axis=1)

fig_violencias_mes = px.bar(quantidade_por_mes, x="Mes", y="Quantidade", color="Quantidade", title="Distribuição do número de violencias por mês")
fig_violencias_mes.update_layout(xaxis_title= "Mês", yaxis_title= "Quantidade")

st.plotly_chart(fig_violencias_mes, use_container_width=True)

col1, col2 = st.columns(2)

#Gráfico 02
contagem_idade = df["NU_IDADE_N"].value_counts()

fig_por_idade = px.bar(contagem_idade, x=contagem_idade.index, y=contagem_idade.values, color=contagem_idade.index, title= "Distribuição do número de violencias por idade", text_auto=True, labels={'NU_IDADE_N': 'Quantidade'})

fig_por_idade.update_layout(title_font_size=25, title_font_color="black", title_x=0.5, xaxis_title= "Idade", yaxis_title= "Quantidade")

col1.plotly_chart(fig_por_idade, use_container_width=True)

#Gráfico 03
contagem_raca = df["CS_RACA"].value_counts()

fig_por_raca = px.bar(contagem_raca, x=contagem_raca.index, y=contagem_raca.values, color=contagem_raca.index, title= "Distribuição do número de violencias por raça", text_auto=True, labels={'CS_RACA': 'Raça'})

fig_por_raca.update_layout(title_font_size=25, title_font_color="black", title_x=0.5, xaxis_title= "Raça", yaxis_title= "Quantidade")

col2.plotly_chart(fig_por_raca, use_container_width=True)