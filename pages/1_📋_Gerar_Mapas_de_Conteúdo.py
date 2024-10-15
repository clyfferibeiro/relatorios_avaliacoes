import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


@st.dialog("🚨 Erro: sem dados da avaliação!")
def func_disciplina():
    st.write(f"Primeiramente, preencha todos os dados da avaliação.")
    if st.button("OK"):
        st.rerun()
    

def update():
    for idx, change in st.session_state.changes["edited_rows"].items():
        for label, value in change.items():
            st.session_state.df.loc[idx, label] = value


def clear_text():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""
    st.session_state.nome_aval = st.session_state.widget_nome_aval
    
def clear_dados():
    st.session_state.nome_aval = st.session_state.widget_nome_aval
    st.session_state.widget_nome_aval = ""
    st.session_state.disciplina = None
    st.session_state.turma = None

# Show app title and description.
st.set_page_config(page_title="App Geração Relatório de Avaliações", page_icon="📋")
st.title("📋 Gerador de Mapa de Conteúdos")
st.info(
    """
    Aplicativo para criação de Mapa de Conteúdos das avaliações.
    """, icon='📋'
)
st.markdown("---")
alunos = pd.read_excel('alunos.xls')

with st.sidebar:
    st.image("logo.png")



st.header("Dados da Avaliação")
with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        disciplina = st.selectbox(
            "**Selecione a Disciplina**",
            ["Matemática", "Português", "Ciências", "Geografia", "História", "Inglês", "Espanhol", "Produção Textual", "Literatura", "Física", "Química", "Biologia" ],
            index=None, key='disciplina'
        )

    with col2:
        turma = st.selectbox("**Selecione a Turma**", alunos['Série'].sort_values(ascending = True).unique(), index=None, key='turma')
    #     "Selecione a Turma",
    #     ["6º Ano", "7º Ano", "8º Ano", "9º Ano", "1ª Série", "2ª Série", "3ª Série"]
    # )
    st.text_input('**Digite o "Nome" da Avaliação** (Teste Mensal, Prova Trimestral, etc...)', key='widget_nome_aval')
    nome_avaliacao = st.session_state.get('nome_aval', '')
    #nome_avaliacao = st.text_input('**Digite o "Nome" da Avaliação** (Teste Mensal, Prova Trimestral, etc...)')
    nome_avaliacao = nome_avaliacao.replace(' ', '_')
# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    # np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
    
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"Q{i}" for i in range(1, 1, 1)],
        "Conteúdo": np.random.choice(issue_descriptions, size=0),
        "Gabarito": np.random.choice(["Aberta", "A", "B", "C", "D", "E"], size=0),
        "Valor": 0.0,
        "Dificuldade": np.random.choice(["Fácil", "Média", "Difícil"], size=0),
        "Série": "",
        # "Date Submitted": [
        #     datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
        #     for _ in range(1)
        # ],
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df


# Show a section to add a new ticket.
st.header("Adicionar Questão")
col5, col6, col7 = st.columns(3)
# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form", clear_on_submit=True):
    #issue = st.text_input("Conteúdo da Questão")
    st.text_input("Conteúdo da Questão", key='widget')
    issue = st.session_state.get('my_text', '')
    col8, col9, col10 = st.columns(3)
    gabarito = col8.selectbox("Gabarito", ["Aberta", "A", "B", "C", "D", "E"])
    valor = col9.number_input("Insira o valor da questão", value=1.0, step=0.10)
    priority = col10.selectbox("Dificuldade", ["Fácil", "Média", "Difícil"])
    submitted = st.form_submit_button("Adicionar", on_click=clear_text)

if submitted:
    if not (disciplina and turma and nome_avaliacao):
        func_disciplina()
    else:
        # Make a dataframe for the new ticket and append it to the dataframe in session
        # state.
        if len(st.session_state.df)==0:
            recent_ticket_number = 0
        else:  
            recent_ticket_number = len(st.session_state.df)
        today = datetime.datetime.now().strftime("%m-%d-%Y")
        if recent_ticket_number < 9:
            id = f'Q0{recent_ticket_number+1}'
        else:
            id = f'Q{recent_ticket_number+1}'
        df_new = pd.DataFrame(
            [
                {
                    "ID": id,
                    "Conteúdo": issue,
                    "Gabarito": gabarito,
                    "Valor": valor,
                    "Dificuldade": priority,
                    "Série": turma,
                    # "Date Submitted": today,
                }
            ]
        )

        # Show a little success message.
        #st.write("Ticket submitted! Here are the ticket details:")
        #st.dataframe(df_new, use_container_width=True, hide_index=True)
        st.session_state.df = pd.concat([ st.session_state.df,df_new], axis=0, ignore_index=True)


st.header("Lista de Questões Adicionadas")
with st.container(border=True):
    col5, col6, col7 = st.columns(3)
    col5.write(f"Número de Questões: `{len(st.session_state.df)}`")
    col6.write(f"Disciplina: `{disciplina}`")
    col7.write(f"Turma: `{turma}`")




    # Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
    # cells. The edited data is returned as a new dataframe.
    st.session_state.df = st.data_editor(
        st.session_state.df, key="changes", on_change=update,
        #num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Gabarito",
                help="Ticket status",
                options=["A","B","C", "D", "E", "Aberta"],
                required=True,
            ),
            "Priority": st.column_config.SelectboxColumn(
                "Dificuldade",
                help="Priority",
                options=["Fácil", "Média", "Difícil"],
                required=True,
            ),
            #"Série": None,
        },
        # Disable editing the ID and Date Submitted columns.
        #disabled=["ID"],
        
    )
    #st.session_state.df = 
    edited_df = st.session_state.df

    st.write(f"Valor Total das Questões: `{edited_df.Valor.sum().round(2)}`")
    st.info(
        "Você pode editar o conteúdo, o gabarito, o valor e a dificuldade das questões clicando duas vezes"
        " na célula correspondente!",
        icon="✍️",
    )

#save = st.form_submit_button("Salvar Planilha")


col3, col4 = st.columns([1, 2], gap="small")#, vertical_alignment="center")
with col3:
    csv = edited_df.to_csv(index=False).encode('utf-8')
    #disciplina = "Matematica"
    st.download_button(
    "Salvar Mapa de Conteúdos",
    csv,
    f'{disciplina}_{turma}_{nome_avaliacao}_Mapa_Conteudos.csv',
    "text/csv",
    key='download-csv'
    )

with col4:
    if st.button("Recomeçar Construção", on_click=clear_dados):
        del st.session_state.df
        #st.session_state.df = pd.DataFrame()
        st.rerun()

# csv = edited_df.to_csv(index=False).encode('utf-8')
# #disciplina = "Matematica"
# st.download_button(
#    "Salvar Mapa de Conteúdos",
#    csv,
#    f'{disciplina}_{turma}_Mapa_Conteudos.csv',
#    "text/csv",
#    key='download-csv'
# )



# columns = edited_df.columns.values.tolist()

# deletar = st.button("Apagar Planilha")

# if deletar:
#     #edited_df
#     st.session_state.df = pd.DataFrame(None)
    

