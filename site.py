import streamlit as st # Site
import ConfigAPI as ca


st.set_page_config(page_title="Extrator de Dados", layout="centered")

st.title("🔍 Extrator de Dados do Maps")


# Campos de input
with st.form("formulario"):
    url = st.text_input("Cole o link da busca no Google Maps:") # Campo de texto para o link
    quantidade = st.number_input("Quantos resultados deseja extrair?", min_value=1, step=1) # Campo numérico para quantidade
    enviar = st.form_submit_button("🚀 Extrair Dados")

if enviar:
    if not url or not quantidade:
        st.warning("Por favor, preencha todos os campos.")
    else:
        df = ca.config_extrator(url, quantidade) # chamando a função do outro arquivo para fazer a extração
        st.success("✅ Dados extraídos com sucesso!")

















