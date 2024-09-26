import pandas as pd
import streamlit as st

# if "data" not in st.session_state:
#     st.session_state["data"] = pd.DataFrame(
#         {
#             "Questão": [],
#             "Conteúdo": [],
#             "Gabarito": [],
#         }
#     )

# data2 = {
#     "Questão": [],
#     "Conteúdo": [],
# }

uploaded_file = st.file_uploader("Faça o upload do Arquivo Desejado", type='csv')
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    nome_arquivo = uploaded_file.name.replace('.csv', '')
    nome_arquivo = nome_arquivo.replace('_Mapa_Conteudos', '')
    nome_arquivo = nome_arquivo.replace('_', ' - ')


    st.write(f'Mapa de Conteúdos Selecionado: {nome_arquivo}')

    st.dataframe(
    data,hide_index=True)
    


    @st.dialog("Adicionar uma Questão")
    def add_fund():
        fund = st.number_input("Número da Questão", min_value=len(st.session_state["data"])+1, step=1)
        asset_class = st.text_input("Conteúdo", "Digite o conteúdo aqui")
        weight = st.selectbox(
            "Gabarito", options=["Aberta","A","B","C","D","E"]
        )
        
    planilha = data 
    #planilha
    planilha_transpose = planilha.T
    #planilha_transpose

    lista = []

    for elemento in planilha_transpose.loc['ID', :]:
        lista.append(f'{elemento}')

    #lista

    alunos = pd.read_csv('alunos_3serie.csv')

    alunos = alunos["Alunos"].values.tolist()

    #alunos
    df = pd.DataFrame({"Alunos": alunos})
    listofzeros = [0.0] * (len(alunos) + 1)

    for i in range(len(lista)):
        df_teste = pd.DataFrame({lista[i]: listofzeros})
        tabela_pontos = df.join(df_teste)
        df = tabela_pontos


    tabela_pontos = st.data_editor(tabela_pontos, use_container_width=True, hide_index=True,)
    
    csv = tabela_pontos.to_csv(index=False).encode('utf-8')
#disciplina = "Matematica"
    st.download_button(
    "Salvar Tabela Pontuação",
    csv,
    f'{nome_arquivo}_Tabela_Pontuação.csv',
    "text/csv",
    key='download-csv'
)