import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import glob
import math

st.set_page_config(layout="wide",page_title="Análise por Turma e Disciplina", page_icon="📊")
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

#st.markdown("# Tabela de Notas - Matemática 8º Ano")

uploaded_file = st.file_uploader("Faça o upload do Arquivo Desejado", type='csv')
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    nome_arquivo = uploaded_file.name.replace('.csv', '')


    notas = data #pd.read_csv('matematica_9_ano.csv')
    #conteudos = pd.read_csv('matematica_9_ano_conteudos.csv')


    grades_valor = notas[notas["Alunos"]=="Valor"]
    grades_valor
    notas = notas.drop(0)
    #notas
    #conteudos
    columns = notas.columns.values.tolist()
    #columns
    notas_questoes = notas
    #notas_questoes

    alunos = notas["Alunos"]

    #alunos = alunos.drop(0)
    alunos = alunos.values.tolist()
    #alunos


    lista = []
    for i in alunos:
        grades = notas[notas["Alunos"]==i]
        #grades
        
        #valor = 1.0 #notas[notas["Alunos"]=="Valor"]
        #grades = grades.str.replace(',','.')
        #yy = (dados[disciplina].str.replace(',','.'))
        #grades
        for j in columns[1:len(columns)]:
            #grades = grades[j].str.replace(',','.')
            valor = grades_valor[j][0]
            #print("Valor")
            #print(valor)
            media_questao = notas_questoes[j]
            #media_questao
            #media_questao = pd.to_numeric(media_questao)
            #media_questao1
            media_questao1 = media_questao.mean()
            #media_questao1submitted = st.form_submit_button("Adicionar")
            a = float(grades[j].values.tolist()[0])
            b = valor #float(valor[j].values.tolist()[0].replace(',','.'))
            nota_perc = round(a/b*100)
            # if nota_perc == 0.0:
            #      nota_perc = 0.1
            delta =  round(nota_perc - media_questao1/b*100) 
            lista.append([i, j, nota_perc, round(media_questao1/b*100), delta ])

    df_media = pd.DataFrame(lista, columns=['Aluno', 'Questão', "Nota", "Media Turma", "Diferença"])

    #df_media   

    for i in alunos:
        grades = notas[notas["Alunos"]==i]
        grades_wa = grades.drop('Alunos', axis=1)
        #grades_wa
        nota_total = grades_wa.sum(axis=1).values
        #nota_total = nota_total1.iat[1, 0]
        df_plot = df_media[df_media["Aluno"]==i]
        #df_plot
        colors = np.ones(len(df_plot["Nota"]))
        colors = np.transpose(colors)
        index1 = df_plot["Nota"] < df_plot["Media Turma"].values
        colors[index1] = 0
        df_plot = df_plot.assign(colors=colors.astype('str'))
        
        # st.dataframe(df_plot,
        #              column_config={"colors": None, "Aluno": None}, hide_index=True)

        fig = px.bar(df_plot, x="Nota", y="Questão", orientation='h', #title=f' Notas de {i} - Matemática ',
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
        #fig.update(layout_showlegend=False)
            # fig_media_porcentage.add_shape( # add a horizontal "target" line
            # type="line", line_color="salmon", line_width=4, opacity=1, line_dash="dot",
            # x0=0, x1=1, xref="paper", y0=70, y1=70, yref="y")

        

        # df_plot = df_plot.style.applymap(color_survived, subset=['Diferença'])
        df_plot = df_plot.style.map(color_survived, subset=['Diferença'])
        #st.dataframe(df.style.applymap(color_survived, subset=['Survived']))
        print(type(nota_total))

        st.markdown("---")
        st.header(f' Notas de {i} - Matemática. Total = {nota_total} pontos')
        with st.container(border=True, height=1000):
            col1, col2 = st.columns([1, 2], vertical_alignment="center")
            with col1:
                st.dataframe(df_plot, column_config={"colors": None, "Aluno": None}, hide_index=True, height=800 )

            with col2:
                fig
        