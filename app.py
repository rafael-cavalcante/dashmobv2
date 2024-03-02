import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Divm",
    page_icon="📊",
    layout="wide")

df = pd.read_csv("dados_violencia_mulheres_ses_2023.csv", delimiter=";")

st.title("📊 DIVM: Um Dashboard de Informação sobre a Violência contra Mulher - 2023")

st.header("Painel sobre casos de Violência `version 1`")

#Variáveis 
meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
         7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

mapeamento = {'0-9': 10, '10-19': 9, '20-29': 8, '30-39': 7, '40-49': 6, '50-59': 5, '60-69': 4, '70-79': 3, '80-89': 2, '90-99': 1, '100+': 0}

mapeamento_inverso = {10: '0-9', 9: '10-19', 8: '20-29', 7: '30-39', 6: '40-49', 5: '50-59', 4: '60-69' , 3: '70-79', 2: '80-99', 1: '90-99',  0: '100+'}

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

#Gráfico 02
df['Total_Viol'] = df[['VIOL_FISIC', 'VIOL_PSICO', 'VIOL_SEXU']].apply(lambda row: (row == 'Sim').sum(), axis=1)

df_grouped = df.groupby('DT_NOTIFIC')['Total_Viol'].sum().reset_index()

fig_contagem_viol = px.line(df_grouped, x='DT_NOTIFIC', y='Total_Viol', title='Contagem total de violações por mês')
fig_contagem_viol.update_layout(xaxis_title="Mês", yaxis_title="Quantidade")

st.plotly_chart(fig_contagem_viol, use_container_width=True)

col1, col2 = st.columns(2)

#Gráfico 03
contagem_idade = df["NU_IDADE_N"].value_counts()

fig_por_idade = px.bar(contagem_idade, x=contagem_idade.index, y=contagem_idade.values, color=contagem_idade.index, title= "Distribuição do número de violencias por idade", text_auto=True, labels={'NU_IDADE_N': 'Quantidade'})
fig_por_idade.update_layout(xaxis_title= "Idade", yaxis_title= "Quantidade")

col1.plotly_chart(fig_por_idade, use_container_width=True)

#Gráfico 04
contagem_raca = df["CS_RACA"].value_counts()

fig_por_raca = px.bar(contagem_raca, x=contagem_raca.index, y=contagem_raca.values, color=contagem_raca.index, title= "Distribuição do número de violencias por raça", text_auto=True, labels={'CS_RACA': 'Raça'})
fig_por_raca.update_layout(xaxis_title= "Raça", yaxis_title= "Quantidade")

col2.plotly_chart(fig_por_raca, use_container_width=True)

col3, col4 = st.columns(2)

#Gráfico 05
violencia_orient_sexual = df["ORIENT_SEX"].value_counts()

fig_orient_sexual = px.pie(violencia_orient_sexual, values=violencia_orient_sexual.values, names=violencia_orient_sexual.index, color=violencia_orient_sexual.index, title="Distribuição do número de violencias por orientação sexual")

col3.plotly_chart(fig_orient_sexual, use_container_width=True)

#Gráfico 06
contagem_cidades = df['ID_MN_RESI'].value_counts().head(10)

fig_10cidades = px.pie(contagem_cidades, values=contagem_cidades, names=contagem_cidades.index, title="Top 10 munícipiso com maior número de violencias", color=contagem_cidades.index)

col4.plotly_chart(fig_10cidades, use_container_width=True)

#Gráfico 07
# Seu código para criar a coluna 'FAIXA_ETARIA'
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120]
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100+']
df['FAIXA_ETARIA'] = pd.cut(df['NU_IDADE_N'], bins=bins, labels=labels, right=False)

lesao_autop = df.groupby('LES_AUTOP').size().sort_values(ascending=False).head(10).reset_index()
df2 = df[df['LES_AUTOP'].isin(lesao_autop['LES_AUTOP'])]
dataset_les_autop = df2.groupby(['LES_AUTOP', 'FAIXA_ETARIA']).size().sort_values(ascending=False).reset_index()

dataset_les_autop.rename(columns={0: 'Quantidade'}, inplace=True)

# Definindo a ordem desejada das faixas etárias
dataset_les_autop['FAIXA_ETARIA'] = dataset_les_autop['FAIXA_ETARIA'].replace(mapeamento)

dataset_les_autop = dataset_les_autop.sort_values('FAIXA_ETARIA', ascending=True)

dataset_les_autop['FAIXA_ETARIA'] = dataset_les_autop['FAIXA_ETARIA'].replace(mapeamento_inverso)

fig_les_autop = px.bar(dataset_les_autop, x='FAIXA_ETARIA', y='Quantidade', color='LES_AUTOP', barmode='group', title="Distribuição de número de lesões auto pessoal por faixa etária",
                                text='Quantidade', labels={'LES_AUTOP': 'Lesão autopessoal', 'FAIXA_ETARIA': 'Faixa Etária'})

fig_les_autop.update_layout(xaxis_title="Idade", yaxis_title="Quantidade")

st.plotly_chart(fig_les_autop, use_container_width=True)

col5, col6 = st.columns(2)

#Gráfico 08
contagem_violencia = df.groupby(['VIOL_FISIC', 'VIOL_PSICO', "VIOL_SEXU"]).size().reset_index(name='Quantidade')

fig_tipo_violencia = px.histogram(contagem_violencia, x=["VIOL_FISIC", "VIOL_PSICO", "VIOL_SEXU"], y="Quantidade", title="Distribuição do número de violencias por tipo", text_auto=True, labels={'variable': 'Tipo Violencia'})
fig_tipo_violencia.update_layout(xaxis_title= "Classificação", yaxis_title= "Quantidade")

col5.plotly_chart(fig_tipo_violencia, use_container_width=True)

#Gráfico 09
df_envolvimento_sexo = df.groupby(["NUM_ENVOLV", "AUTOR_SEXO"]).size().reset_index(name='Quantidade')

fig_envolvimento_sexo = px.histogram(df_envolvimento_sexo, x="NUM_ENVOLV", y="Quantidade",  color="AUTOR_SEXO",title="Distribuição do número de violencias por sexo autor e numero de envolvidos", text_auto=True, labels={'AUTOR_SEXO': 'Sexo Autor'})
fig_envolvimento_sexo.update_layout(xaxis_title= "Número Envolvidos", yaxis_title= "Quantidade")

col6.plotly_chart(fig_envolvimento_sexo, use_container_width=True)

#Gráfico 10
df_municipio_ocorrido = df.groupby(["ID_MN_RESI", "LOCAL_OCOR"]).size().reset_index(name="Quantidade")

df_municipio_ocorrido_max_sorted = df_municipio_ocorrido.sort_values(by="Quantidade", ascending=False).head(10)

df_municipio_ocorrido_max_sorted = df_municipio_ocorrido_max_sorted.sort_values("Quantidade", ascending=True)

fig_municipio_ocorrido = px.bar(df_municipio_ocorrido_max_sorted, x="Quantidade", y="ID_MN_RESI", color="LOCAL_OCOR",
             title='TOP 10 Municípios com maior número de Ocorrência e Local', labels={'LOCAL_OCOR': 'Local'})
fig_municipio_ocorrido.update_layout(xaxis_title= "Quantidade", yaxis_title= "Município")

st.plotly_chart(fig_municipio_ocorrido, use_container_width=True)

col7, col8 = st.columns(2)

#Gráficos Dinâmicos
df_municipios = df['ID_MN_RESI'].unique()

list_municipios = list(df_municipios)

list_municipios.insert(0, "TODOS")

cidade_selecionada = st.selectbox("Município", list_municipios)

if(cidade_selecionada == "TODOS"):
    df_cidade = df
else:
    df_cidade = df[df['ID_MN_RESI'] == cidade_selecionada]
    
col7, col8 = st.columns(2)

df_cidade['Total_Viol'] = df_cidade[['VIOL_FISIC', 'VIOL_PSICO', 'VIOL_SEXU']].apply(lambda row: (row == 'Sim').sum(), axis=1)

df_grouped = df_cidade.groupby('DT_NOTIFIC')['Total_Viol'].sum().reset_index()

fig_contagem_viol_por_cidade = px.line(df_grouped, x='DT_NOTIFIC', y='Total_Viol', title=f'Contagem total de violações por mês em {cidade_selecionada}')
fig_contagem_viol_por_cidade.update_layout(xaxis_title="Mês", yaxis_title="Quantidade")

col7.plotly_chart(fig_contagem_viol_por_cidade, use_container_width=True)

df_envolvimento_sexo_cidade = df_cidade.groupby(["NUM_ENVOLV", "AUTOR_SEXO"]).size().reset_index(name='Quantidade')

fig_envolvimento_sexo_cidade = px.histogram(df_envolvimento_sexo_cidade, x="NUM_ENVOLV", y="Quantidade",  color="AUTOR_SEXO",title=f"Distribuição do número de violencias <br>por sexo autor e numero de envolvidos em {cidade_selecionada}", text_auto=True, labels={'AUTOR_SEXO': 'Sexo Autor'})
fig_envolvimento_sexo_cidade.update_layout(xaxis_title= "Número Envolvidos", yaxis_title= "Quantidade")

col8.plotly_chart(fig_envolvimento_sexo_cidade, use_container_width=True)