import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide",page_title="App Geração Relatório de Avaliações", page_icon="📊")
st.markdown(
    """
    <style type="text/css" media="print">
      hr
      {
        page-break-after: always;
        page-break-inside: avoid;
      }
    </style>
""",
    unsafe_allow_html=True,
)

def color_survived(val):
            color = 'blue' if val>0 else 'red'
            return f'background-color: {color}'

st.title("📊 Gerador de Relatórios")
st.write(
    """
    Selecione abaixo o arquivo da Tabela de Questões.
    """
)

uploaded_file = st.file_uploader("**Faça o upload do Arquivo Desejado**", type='csv')
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    nome_arquivo = uploaded_file.name.replace('.csv', '')


    notas = data 

    notas_com_conteudos = notas
    columns = notas.columns.values.tolist()
    busca = 'Conteudo'
    lista_conteudos = []
    for s in columns:
         if busca in s:
              lista_conteudos.append(notas[s][0])
              notas = notas.drop(s, axis=1)
              
           
    grades_valor = notas[notas["Alunos"]=="Valor"]
    grades_valor = grades_valor.drop('Alunos', axis=1)
    valor_total = grades_valor.sum(axis=1)

    
    notas = notas.drop(0)
    columns = notas.columns.values.tolist()
    notas_questoes = notas

    alunos = notas["Alunos"]
    alunos = alunos.values.tolist()


    lista = []
    for i in alunos:
        grades = notas[notas["Alunos"]==i]
        for j in columns[1:len(columns)]:
            valor = grades_valor[j][0]
            media_questao = notas_questoes[j]
            media_questao1 = media_questao.mean()
            a = float(grades[j].values.tolist()[0])
            b = valor #float(valor[j].values.tolist()[0].replace(',','.'))
            nota_perc = round(a/b*100)
            delta =  round(nota_perc - media_questao1/b*100) 
            lista.append([i, j, nota_perc, round(media_questao1/b*100), delta ])

    df_media = pd.DataFrame(lista, columns=['Aluno', 'Questão', "Nota", "Media Turma", "Diferença"])

    for i in alunos:
        grades = notas[notas["Alunos"]==i]
        grades_wa = grades.drop('Alunos', axis=1)
        nota_total = grades_wa.sum(axis=1)
        df_plot = df_media[df_media["Aluno"]==i]
        colors = np.ones(len(df_plot["Nota"]))
        colors = np.transpose(colors)
        index1 = df_plot["Nota"] < df_plot["Media Turma"].values
        colors[index1] = 0
        df_plot = df_plot.assign(colors=colors.astype('str'))
        

        fig = px.bar(df_plot, x="Nota", y="Questão", orientation='h', 
                            text_auto = True, width=800, height=800,
                            labels={
                                        "media": "Média Percentual (%)",
                                        "disciplina": "Disciplinas",
                                        "colors": ''
                        },
                        color="colors",
                        color_discrete_map={ '1.0': 'blue', '0.0': 'red'}).update_xaxes(categoryorder="total ascending")
        newnames = {'0.0':'Abaixo da Média da Turma', '1.0': 'Acima da Média da Turma'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
        fig.update_layout(barmode='stack', yaxis={'categoryorder':'category ascending'})

       
        df_plot["Conteúdo"] = lista_conteudos
        df_plot = df_plot.style.map(color_survived, subset=['Diferença'])
        st.markdown("---")
        st.header(f' Notas de {i}. Pontuação: {nota_total[alunos.index(i)+1]}/{valor_total[0].round(1)} ou {(nota_total[alunos.index(i)+1] / valor_total[0].round(1) *100).round(1)}%')
        with st.container(border=True, height=1000):
            col1, col2 = st.columns([1, 2], vertical_alignment="center")
            with col1:
                st.dataframe(df_plot, column_config={"colors": None, "Aluno": None}, hide_index=True, height=800 )

            with col2:
                fig
        
