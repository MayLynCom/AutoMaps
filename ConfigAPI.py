import requests # Fazer conexões
import pandas as pd # Tratamento de dados
import math  # Biblioteca para operações matemáticas (arredondar número de páginas)
from urllib.parse import urlparse #Manipular a URL
import streamlit as st # Site


# ===========================
# CONFIGURAÇÃO DA URL
# ===========================


def config_extrator(url, quantidade):
    parsed = urlparse(url)  # Pega a URL e atribui a função parse
    path = parsed.path  # aqui ele vai mostrar tudo que vier depois do dominio, ou seja o caminho todo
    parts = path.split('/')  # aqui você esta dizendo que a barra é o que divide cada informação da url

    term = parts[3]
    coords = parts[4]

    term = term.replace('+', '_')  # Transforma o + em _

    # ===========================
    # CONFIGURAÇÃO DA API
    # ===========================

    API_KEY = "9d3659aacc443aca0a7475f087d05f36b8e42a3d61221a8c232cb77c7dc1a435"  # 🔥 Coloque sua chave da SerpApi aqui

    # ===========================
    # PARÂMETROS DA BUSCA FIXOS
    # ===========================

    base_url = "https://serpapi.com/search"
    base_params = {
        "engine": "google_maps",  # Motor de busca: Google Maps
        "q": term,  # Palavra-chave da busca
        "ll": coords,  # Coordenadas (latitude, longitude, zoom)
        "type": "search",  # Tipo de busca (search padrão)
        "api_key": API_KEY  # Sua chave da API
    }

    # ===========================
    # INPUT DO USUÁRIO
    # ===========================

    # Cada página retorna até 20 resultados, então calculamos quantas páginas são necessárias
    # Usamos math.ceil para arredondar pra cima, garantindo que tenha resultados suficientes
    numero_paginas = math.ceil(quantidade / 20)

    print(f"\n🔄 Buscando {quantidade} resultados em {numero_paginas} páginas...\n")


    # ===========================
    # FUNÇÃO PARA EXTRAIR A PÁGINA BASEADA NO PARAMETRO START, SE FOR 20 É A PRIMEIRA SE FOR 40 A SEGUNDA ETC
    # ===========================

    def extrair_dados(start):
        # Copia os parâmetros base e adiciona o 'start' que controla a paginação
        params = base_params.copy()
        params["start"] = start
        # Faz a requisição para a API
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()  # Retorna a resposta em JSON
        else:
            # Se der erro, mostra o erro e retorna None
            print(f"❌ Erro na requisição: {response.status_code}")
            print(response.text)
            return None

    # ===========================
    # LOOP PARA EXTRAIR DADOS
    # ===========================

    dados_extraidos = []  # Lista onde os dados vão ser armazenados

    for pagina in range(numero_paginas):
        # O parâmetro 'start' é sempre pagina * 20 → 0, 20, 40, 60...
        start = pagina * 20
        resultado = extrair_dados(start)

        if resultado and "local_results" in resultado:  # Aqui ele verifica se teve extração dos dados e tem o local results dentro de resultado
            for item in resultado["local_results"]:  # Aqui ele percorre a lista dos resultados dos locais
                dados = {  # Aqui ele ta extraindo os dados que vem em JSON para colocar em um dicionário
                    "Nome": item.get("title"),
                    "Endereço": item.get("address"),
                    "Telefone": item.get("phone"),
                    "Nota": item.get("rating"),
                    "Nº Avaliações": item.get("reviews"),
                    "Website": item.get("website"),
                    "Horário": item.get("hours"),
                }
                dados_extraidos.append(dados)  # Adiciona o dicionário em uma lista

            print(f"✅ Página {pagina + 1} coletada com sucesso!")
        else:
            print(f"⚠️ Nenhum resultado encontrado na página {pagina + 1}")

    # ===========================
    # TRATAR SE EXTRAIU MAIS QUE O PEDIDO
    # ===========================

    # Corta a lista para ter exatamente a quantidade que o usuário pediu (às vezes vem mais na última página)
    dados_extraidos = dados_extraidos[:quantidade]

    # ===========================
    # ORGANIZANDO OS DADOS EM PLANILHA
    # ===========================

    # Pega os dados dentro da lista e organiza em tabela/planilha
    df = pd.DataFrame(dados_extraidos)

    # ===========================
    # MOSTRANDO OS DADOS NO SITE
    # ===========================

    st.markdown("### 👇 Primeiros 3 resultados encontrados:")
    st.dataframe(df.head(3))  # Mostra só os 3 primeiros

    # Botão de download
    st.download_button(
        label="📥 Baixar CSV",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="resultados.csv",
        mime="text/csv"
    )




"""# ===========================
# SALVANDO EM CSV
# ===========================

df.to_csv(f"{term}.csv", index=False, encoding="utf-8-sig")
print(f"\n📁 Arquivo {term}.csv salvo com sucesso!")"""
