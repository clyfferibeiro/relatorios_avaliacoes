import pandas as pd
import streamlit as st

st.set_page_config(layout="wide",page_title="App Geração Relatório de Avaliações", page_icon="🔢")

st.title("🔢 Gerador de Tabela de Pontuações")

st.info(
    """
    Aplicativo para criação de Tabela de Pontuação das avaliações.
    """, icon='⌨️'
)
st.markdown("---")
with st.sidebar:
    st.image("logo.png")



css='''
<style>
[data-testid="stFileUploaderDropzone"] div div::before {color:black; content:"Arraste e Solte o arquivo aqui"}
[data-testid="stFileUploaderDropzone"] div div span{display:none;}
[data-testid="stFileUploaderDropzone"] div div::after {color:black; font-size: .8em; content:"Limite por arquivo: 200 MB"}
[data-testid="stFileUploaderDropzone"] div div small{display:none;}
[data-testid="stFileUploaderDropzone"] button {border: solid 2px white;font-size: 0;width: 38%;}
[data-testid="stFileUploaderDropzone"] button::after {content:"Procurar Arquivo";display: block;position: absolute;font-size: 15px;} 
</style>
'''
st.markdown(css, unsafe_allow_html=True)

col1, col2 = st.columns([3,2])


with col1:
    st.write(
        """
        👇 Selecione abaixo o arquivo do Mapa de Conteúdos da Avaliação.
        """
    )

    uploaded_file = st.file_uploader("**Faça o upload do Arquivo Desejado**", type='csv')
i = 0
l = 0
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    nome_arquivo = uploaded_file.name.replace('.csv', '')
    nome_arquivo = nome_arquivo.replace('_Mapa_Conteudos', '')
    nome_arquivo_relatorio = nome_arquivo.replace('_', ' - ')

    if 'ID' in data.columns:

        st.write(f'**Mapa de Conteúdos Selecionado: {nome_arquivo_relatorio}**')

        st.dataframe(data,hide_index=True)

        st.info(
                "Insira as notas dos alunos abaixo e salve a Tabela de Pontuação.",
                icon="✍️",
                )
        


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

        #print(type(lista3[0]))
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
        while i < len(lista):
            for j in range(len(lista3)):
                list = [ float(lista3[j]) ]
                list.extend(listofzeros)
            
                df_teste = pd.DataFrame({lista[i]:list})
                tabela_pontos = df.join(df_teste)
                
                df = tabela_pontos
                i = i + 1
                #print(i)

        
        tabela_pontos = st.data_editor(tabela_pontos, use_container_width=True, hide_index=True)
        
        cont_questao = []
        for j in range(len(lista)):
            cont_questao.append(lista[j]+"Conteudo")

        
        while l < len(cont_questao):
            for j in range(len(lista2)):
                list1 = []
                for k in range(len(alunos)+1):
                    list1.append(lista2[j])
                #list1
                df_teste = pd.DataFrame({cont_questao[l]:list1})
                new_tabela_pontos = tabela_pontos.join(df_teste)
                tabela_pontos = new_tabela_pontos
                l = l + 1

        #cont_questao
        #lista2
        #new_tabela_pontos
        csv = tabela_pontos.to_csv(index=False).encode('utf-8')
    #disciplina = "Matematica"
        st.download_button(
        "Salvar Tabela Pontuação",
        csv,
        f'{nome_arquivo}_Turma_{turma}_Tabela_Pontuação.csv',
        "text/csv",
        key='download-csv'
        )
    else:
        st.error("🚨 DADOS INVÁLIDOS! Verifique se o arquivo é um Mapa de Conteúdos. 🚨")
