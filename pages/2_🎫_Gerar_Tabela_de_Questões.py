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
i = 0
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
    #planilha_transpose
    lista = []
    lista2 = []
    lista3 = []

    for elemento in planilha_transpose.loc['ID', :]:
        lista.append(f'{elemento}')
        

    for elemento in planilha_transpose.loc['Conteúdo', :]:
        lista2.append(f'{elemento}')

    for elemento in planilha_transpose.loc['Valor', :]:
        lista3.append(f'{elemento}')

    print(type(lista3[0]))
    #lista1
    #lista2
    #lista3
    #lista
    alunos = pd.read_excel('alunos.xls')
    #alunos
    alunos = alunos[alunos["Série"]==planilha["Série"][0]]
    #alunos
    turma = st.selectbox("Turma", alunos['Turma'].sort_values(ascending = True).unique())
    alunos = alunos[alunos["Turma"]==turma]
    #alunos
    alunos = alunos["Nome"].values.tolist()
    alunos = ["Valor"] + alunos
    #alunos.insert(0, "Conteúdo")
    #alunos.insert(1, "Valor")
    #alunos
    df = pd.DataFrame({"Alunos": alunos})
    #df
    listofzeros = [0.0] * (len(alunos)-1)
    listofzeros = listofzeros
    #listofzeros
    #lista
    #for i in range(len(lista)):
    #lista3
    #lista
    while i < len(lista):
        for j in range(len(lista3)):
            #list = []
            #print(j)
            #print(lista2[j])
            #list = [ lista2[j] ]
            list = [ float(lista3[j]) ]
            #list.extend(list3)
            list.extend(listofzeros)
            #list
        #for i in range(len(lista)):
            df_teste = pd.DataFrame({lista[i]:list})
            tabela_pontos = df.join(df_teste)
            #df = tabela_pontos
            #df[lista[i]][1] = pd.to_numeric(df[lista[i]][1])
            df = tabela_pontos
            #tabela_pontos = df
            #df
            i = i + 1
            print(i)

    #df2 = df.append(pd.DataFrame(lista2 + lista3,index=['0'],columns=df.columns))
    #df2 = pd.concat([lista2 + lista3,df.loc[:]]).reset_index(drop=True)
    #df2
    
    tabela_pontos = st.data_editor(tabela_pontos, use_container_width=True, hide_index=True)
    #df = st.data_editor(df)
    print(i)


    csv = tabela_pontos.to_csv(index=False).encode('utf-8')
#disciplina = "Matematica"
    st.download_button(
    "Salvar Tabela Pontuação",
    csv,
    f'{nome_arquivo}_Tabela_Pontuação.csv',
    "text/csv",
    key='download-csv'
    )