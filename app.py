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

#Erro nesse gráfico
#Gráfico 02
#contagem_idade = df["NU_IDADE_N"].value_counts().reset_index(name="Quantidade")

#fig_por_idade = px.bar(contagem_idade, x="index", y="Quantidade", color="Quantidade", title= "Distribuição do número de violencias por idade", text_auto=True, labels={'NU_IDADE_N': 'Quantidade'})

#fig_por_idade.update_layout(title_font_size=25, title_font_color="black", title_x=0.5, xaxis_title= "Idade", yaxis_title= "Quantidade")

#fig_por_idade


#st.plotly_chart(fig_por_idade, use_container_width=True)

#Erro nesse gráfico
#Gráfico 03
contagem_raca = df["CS_RACA"].value_counts()

fig_por_raca = px.bar(contagem_raca, x=contagem_raca.index, y=contagem_raca.values, color="CS_RACA", title= "Distribuição do número de violencias por raça", text_auto=True, labels={'CS_RACA': 'Quantidade'})

fig_por_raca.update_layout(title_font_size=25, title_font_color="black", title_x=0.5, xaxis_title= "Raça", yaxis_title= "Quantidade")

st.plotly_chart(fig_por_raca, use_container_width=True)

#Gráfico 04
violencia_orient_sexual = df["ORIENT_SEX"].value_counts()

fig_orient_sexual = px.pie(violencia_orient_sexual, values=violencia_orient_sexual, names=violencia_orient_sexual.index, title="Distribuição do número de violencias por orientação sexual", color=violencia_orient_sexual.index)

fig_orient_sexual.update_layout(title_font_size=25, title_font_color="black", title_x=0.5, title_text='Distribuição do número de violencias por orientação sexual')

st.plotly_chart(fig_orient_sexual, use_container_width=True)

#Gráfico 05
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120]
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100+']
df['FAIXA_ETARIA'] = pd.cut(df['NU_IDADE_N'], bins=bins, labels=labels, right=False)

lesao_autop = df.groupby('LES_AUTOP').size().sort_values(ascending=False).head(10).reset_index()
df2 = df[df['LES_AUTOP'].isin(lesao_autop['LES_AUTOP'])]
dataset_les_autop = df2.groupby(['LES_AUTOP', 'FAIXA_ETARIA']).size().sort_values(ascending=False).reset_index()

dataset_les_autop.rename(columns={0: 'Quantidade'}, inplace=True)

fig_les_autop = px.bar(dataset_les_autop, x='FAIXA_ETARIA', y='Quantidade', color='LES_AUTOP', title="Distribuição de número de lesões por faixa etária",
                                text='Quantidade', labels={'LES_AUTOP': 'Lesão autopessoal', 'FAIXA_ETARIA': 'Faixa Etária'})

fig_les_autop.update_layout(title_font_size=25, title_font_color="black", title_x=0.5, xaxis_title="Idade", yaxis_title="Quantidade")

st.plotly_chart(fig_les_autop, use_container_width=True)

#Gráfico 06
contagem_cidades = df['ID_MN_RESI'].value_counts().head(10)

fig_10cidades = px.pie(contagem_cidades, values=contagem_cidades, names=contagem_cidades.index, title="Distribuição do número de violencias por munícipio", color=contagem_cidades.index)

st.plotly_chart(fig_10cidades, use_container_width=True)

#Gráfico 07
df['Total_Viol'] = df[['VIOL_FISIC', 'VIOL_PSICO', 'VIOL_SEXU']].apply(lambda row: (row == 'Sim').sum(), axis=1)

df_grouped = df.groupby('DT_NOTIFIC')['Total_Viol'].sum().reset_index()

fig_contagem_viol = px.line(df_grouped, x='DT_NOTIFIC', y='Total_Viol', title='Contagem total de violações por mês')

fig_contagem_viol.update_layout(title_font_size=25, title_font_color="black", title_x=0.5, xaxis_title="Mês", yaxis_title="Quantidade")

st.plotly_chart(fig_contagem_viol, use_container_width=True)

#Gráfico 08
# Filtrar os dados onde 'violencia_fisica' é igual a 'sim' ou 'violencia_psicologica' é igual a 'sim'
#df_filtrado = df[(df['VIOL_FISIC'] == 'Sim') | (df['VIOL_PSICO'] == 'Sim') | (df['VIOL_SEXU'] == 'Sim')]

# Agrupar pelos valores das colunas e contar as ocorrências
contagem_violencia = df.groupby(['VIOL_FISIC', 'VIOL_PSICO', "VIOL_SEXU"]).size().reset_index(name='Quantidade')

fig_tipo_violencia = px.histogram(contagem_violencia, x=["VIOL_FISIC", "VIOL_PSICO", "VIOL_SEXU"], y="Quantidade", title="Distribuição do número de violencias por tipo", text_auto=True, labels={'variable': 'Tipo Violencia'})

fig_tipo_violencia.update_layout(xaxis_title= "Classificação", yaxis_title= "Quantidade")

st.plotly_chart(fig_tipo_violencia, use_container_width=True)

#Gráfico 09
df_envolvimento_sexo = df.groupby(["NUM_ENVOLV", "AUTOR_SEXO"]).size().reset_index(name='Quantidade')

fig_envolvimento_sexo = px.histogram(df_envolvimento_sexo, x="NUM_ENVOLV", y="Quantidade",  color="AUTOR_SEXO",title="Distribuição do número de violencias por sexo autor e numero de envolvidos", text_auto=True, labels={'variable': 'Tipo Violencia'})
fig_envolvimento_sexo.update_layout(xaxis_title= "Número Envolvidos", yaxis_title= "Quantidade")

st.plotly_chart(fig_envolvimento_sexo, use_container_width=True)

#Gráfico 10
df_municipio_ocorrido = df.groupby(["ID_MN_RESI", "LOCAL_OCOR"]).size().reset_index(name="Quantidade")

df_municipio_ocorrido_max = df_municipio_ocorrido.loc[df_municipio_ocorrido.groupby("ID_MN_RESI")["Quantidade"].idxmax()]

df_municipio_ocorrido_max_sorted = df_municipio_ocorrido_max.sort_values(by="Quantidade", ascending=False).head(10)

df_municipio_ocorrido_max_sorted = df_municipio_ocorrido_max_sorted.sort_values("Quantidade", ascending=True)

fig_municipio_ocorrido = px.bar(df_municipio_ocorrido_max_sorted, x="Quantidade", y="ID_MN_RESI", color="LOCAL_OCOR",
             labels={'Casos': 'Número de Casos', 'Municipios': 'Município'},
             title='Número de Casos por Município e Local de Ocorrência')

st.plotly_chart(fig_municipio_ocorrido, use_container_width=True)