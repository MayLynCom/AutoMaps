import streamlit as st
import pandas as pd
import re                                                                                                                           #GPT
import os                                                                                                                           #GPT

# Função para checar se o e-mail é válido
def email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None                                                                   #GPT

# Função para checar se a senha é válida
def senha_valida(senha):
    return (
        len(senha) >= 8                # Mínimo 8 caracteres
        and any(char.isdigit() for char in senha)  # Pelo menos 1 número                                                              #GPT
    )

# Função para checar se e-mail já existe no csv
def email_existe(email):
    if not os.path.exists("usuarios.csv"):
        df = pd.DataFrame(columns=["usuario", "senha"])
        df.to_csv("usuarios.csv", index=False)
    df = pd.read_csv("usuarios.csv")
    return email in df["usuario"].values

# Função para salvar o usuário novo
def salvar_usuario(email, senha):
    df = pd.read_csv("usuarios.csv")
    novo = pd.DataFrame([{"usuario": email, "senha": senha}])
    df = pd.concat([df, novo], ignore_index=True)                                                                               #GPT
    df.to_csv("usuarios.csv", index=False)

# Interface de registro
st.set_page_config(page_title="Cadastro", layout="centered")
st.title("📝 Cadastro de Novo Usuário")

email = st.text_input("E-mail (será seu login)")
senha = st.text_input("Senha (mín. 8 caracteres e pelo menos 1 número)", type="password")
confirmar_senha = st.text_input("Confirme sua senha", type="password")

if st.button("Registrar"):
    # Checa se todos os campos foram preenchidos
    if not email or not senha or not confirmar_senha:
        st.warning("Preencha todos os campos!")
    # Checa se e-mail é válido
    elif not email_valido(email):
        st.warning("Digite um e-mail válido!")
    # Checa se senha é forte
    elif not senha_valida(senha):
        st.warning("Senha deve ter no mínimo 8 caracteres e pelo menos 1 número!")
    # Checa se as senhas são iguais
    elif senha != confirmar_senha:
        st.warning("As senhas digitadas não conferem!")
    # Checa se e-mail já existe
    elif email_existe(email):
        st.error("E-mail já cadastrado!")
    # Salva o usuário se tudo ok
    else:
        salvar_usuario(email, senha)
        st.success("Usuário cadastrado com sucesso! Agora faça login.")

