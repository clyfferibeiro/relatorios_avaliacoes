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
            if val > 0:
                color = 'blue' 
                color_texto = 'white'
            elif val<0: 
                color = 'red'
                color_texto = 'white'
            else:
                  color = 'white'
                  color_texto = 'black'
            return f'background-color: {color}; color: {color_texto}'

def color_questoes(val):
            if val <= 10:
                  color = 'red'
                  color_texto = 'white'
            elif val > 10 and val <= 50:
                  color = 'orange'
                  color_texto = 'white'
            elif val > 50 and val <= 70:
                  color = 'yellow'
                  color_texto = 'black'
            elif val > 70 and val <= 90:
                  color = 'blue'
                  color_texto = 'white'
            elif val > 90:
                  color = 'green'
                  color_texto = 'white'
            return f'background-color: {color}; color: {color_texto}'

def color_media(val):
            if val == 'Média da Questão':
                  return f'color:white; background-color:black; '
            

st.title("📊 Gerador de Relatórios")
st.write(
    """
    Selecione abaixo o arquivo da Tabela de Questões.
    """
)

tamanho = st.sidebar.slider("Tamanho das páginas", 400, 1500, 800)

uploaded_file = st.file_uploader("**Faça o upload do Arquivo Desejado**", type='csv')
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    nome_arquivo = uploaded_file.name.replace('.csv', '')


    notas = data 

    if 'Alunos' in notas.columns:

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


        #notas_questoes

        alunos = notas["Alunos"]
        alunos = alunos.values.tolist()


        lista = []
        lista_notas = []
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
                lista_notas.append([nota_perc])

        df_media = pd.DataFrame(lista, columns=['Aluno', 'Questão', "Nota", "Media Turma", "Diferença"])
        #df_media
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

            # fig.add_trace(df_plot, x="Diferença", y='Questão',
            #         marker_color='crimson')
            #eixo_x = df_plot["Diferença"].to_list()
            #eixo_y = df_plot["Questão"].to_list()
            #eixo_x
            #eixo_y
            
            #fig.add_trace(go.Bar( x = eixo_x, y = eixo_y, showlegend=False ))

                
            fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                        legendgroup = newnames[t.name],
                                        hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                        )
                    )
            fig.update_layout(barmode='stack', yaxis={'categoryorder':'category ascending'})

            #notas_questoes
            #df_plot
            #columns
            #grades_wa
            
            
            
            #notas_questoes
            
            #notas_questoes

            #print(fig.key)
            df_plot["Conteúdo"] = lista_conteudos
            df_plot = df_plot.style.map(color_survived, subset=['Diferença'])
            st.markdown("---")
            st.header(f' Notas de {i}. Pontuação: {nota_total[alunos.index(i)+1].round(2)}/{valor_total[0].round(1)} ou {(nota_total[alunos.index(i)+1] / valor_total[0].round(1) *100).round(1)}%')
            with st.container(border=True, height=tamanho):
                col1, col2 = st.columns([1, 1], vertical_alignment="center")
                with col1:
                    st.dataframe(df_plot, column_config={"colors": None, "Aluno": None}, hide_index=True, height=tamanho )

                with col2:
                    fig
            fig = []

        #grades_valor
        st.markdown("---")
        st.header('Relatório por Item')
        with st.container(border=True, height=tamanho):
            mean_list = ['Média da Questão']
            for m in range(len(columns)-1):
                    notas_questoes[columns[m+1]] = (notas_questoes[columns[m+1]] / grades_valor[columns[m+1]][0] * 100)
                    mean_list.append(round(notas_questoes[columns[m+1]].mean()))

    
            notas_questoes.loc[-1, :] = mean_list
            #notas_questoes
            notas_questoes = notas_questoes.style.map(color_questoes, subset=columns[1:len(columns)])
            notas_questoes = notas_questoes.map(color_media, subset='Alunos')
        
            notas_questoes = notas_questoes.format(precision=0)


            col3, col4 = st.columns([4, 2])#, vertical_alignment="center")
            with col3:
                st.dataframe(notas_questoes, hide_index=True, height=tamanho )

            with col4:
                st.image("legenda.png")
                st.dataframe(df_plot, column_config={"colors": None, "Aluno": None, "Nota": None, "Media Turma": None, "Diferença": None}, hide_index=True, height=tamanho)
            
            

            #notas_questoes.style
    else:
          st.write("DADOS INVÁLIDOS!")
    