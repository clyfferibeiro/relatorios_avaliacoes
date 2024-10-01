import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide", page_title="App Geração Relatório de Avaliações")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


with st.container():
    #st.subheader("Meu primeiro site com o Streamlit")
    st.title("App Geração Relatórios de Avaliações")
    #st.write("Informações sobre notas dos alunos.")
    st.write("Navegue no menu do lado esquerdo para as tarefas desejadas.")
    st.markdown('---')
    st.title('Passos:')
    st.write('**1.** Crie e Salve o Mapa de Conteúdos utilizando a aba ["Gerar Mapa de Conteúdos"](https://relatoriosavaliacoes-6rrmrmsjn4dtuxbkt9qk8x.streamlit.app/Gerar_Mapas_de_Conte%C3%BAdo);')
    st.write('**2.** Gere a Tabela de Pontuação, com base no Mapa de Conteúdos salvo no item 1, utilizando a aba ["Gerar Tabela de Pontuação"](https://relatoriosavaliacoes-6rrmrmsjn4dtuxbkt9qk8x.streamlit.app/Gerar_Tabela_de_Pontua%C3%A7%C3%B5es);')
    st.write('**3.** Gere os relatórios, à partir da Tabela de Pontuação salva anteriormente, utilizando a aba ["Gerar Relatórios"](https://relatoriosavaliacoes-6rrmrmsjn4dtuxbkt9qk8x.streamlit.app/Gerar_Relat%C3%B3rios);')
