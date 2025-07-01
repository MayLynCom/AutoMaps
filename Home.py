import streamlit as st
from streamlit import switch_page
import pandas as pd
import os

# =========================
# FUNÇÃO AUXILIAR PARA VERIFICAR USUÁRIO E SENHA
# =========================

def login_valido(usuario, senha):
    # Lê o CSV e verifica se a combinação usuário+senha existe
    df = pd.read_csv("usuarios.csv")
    usuario_ok = df[(df["usuario"] == usuario) & (df["senha"] == senha)]
    return not usuario_ok.empty

# =========================
# INTERFACE STREAMLIT (LOGIN)
# =========================

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login de Usuário")

usuario = st.text_input("E-mail").lower()  # Campo usuário
senha = st.text_input("Senha", type="password")  # Campo senha


# Cria colunas lado a lado: a segunda maior pra empurrar o botão direito
col1, col2, col3 = st.columns([4.5, 1, 1])


with col1:
    if st.button("Entrar"):
        if not usuario or not senha:
            st.warning("Preencha todos os campos!")
        elif login_valido(usuario, senha):
            switch_page("pages/Automacao.py")
        else:
            st.error("Usuário ou senha incorretos.")

with col3:
    if st.button("Cadastrar"):
        switch_page("pages/Cadastro.py")