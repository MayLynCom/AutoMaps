import streamlit as st
import pandas as pd
import os

# =========================
# FUNÇÃO AUXILIAR PARA VERIFICAR USUÁRIO E SENHA
# =========================

def login_valido(usuario, senha):
    # Garante que existe o arquivo usuarios.csv; se não, cria vazio
    if not os.path.exists("usuarios.csv"):
        df = pd.DataFrame(columns=["usuario", "senha"])
        df.to_csv("usuarios.csv", index=False)
    # Lê o CSV e verifica se a combinação usuário+senha existe
    df = pd.read_csv("usuarios.csv")
    usuario_ok = df[(df["usuario"] == usuario) & (df["senha"] == senha)]
    return not usuario_ok.empty

# =========================
# INTERFACE STREAMLIT (LOGIN)
# =========================

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login de Usuário")

usuario = st.text_input("Usuário")  # Campo usuário
senha = st.text_input("Senha", type="password")  # Campo senha

if st.button("Entrar"):
    # Verifica se ambos estão preenchidos
    if not usuario or not senha:
        st.warning("Preencha todos os campos!")
    elif login_valido(usuario, senha):
        st.success("Usuário encontrado.")
    else:
        st.error("Usuário ou senha incorretos.")


st.markdown("---")
st.markdown("[Cadastrar](./register)")