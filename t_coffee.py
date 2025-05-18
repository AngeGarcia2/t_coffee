# -*- coding: utf-8 -*-
"""
Editor Spyder

Este é um arquivo de script temporário.
"""


# 1. IMPORTAÇÃO DE BIBLIOTECAS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 2. CARREGAMENTO DO DATASET
caminho = r"C:\Users\User\Desktop\t_algebra\coffee_analysis.csv"
df = pd.read_csv(caminho)

# 3. TRANSFORMAÇÃO DO TEXTO EM VETORES TF-IDF

vetorizador = TfidfVectorizer(stop_words='english')
matriz_tfidf = vetorizador.fit_transform(df['desc_1'])


# 4. CÁLCULO DA SIMILARIDADE DO COSSENO
cosine_sim = cosine_similarity(matriz_tfidf, matriz_tfidf)

# 5. TRADUÇÃO DO RESUTLADO DA AVALIAÇÃO SENSORIAL

from googletrans import Translator

tradutor = Translator()

def traduzir_texto(texto, src='en', dest='pt'):
    try:
        return tradutor.translate(texto, src=src, dest=dest).text
    except:
        return "(tradução indisponível)"

def recomendar_cafes(indice_cafe, top_n=5):
    similares = list(enumerate(cosine_sim[indice_cafe]))
    similares = sorted(similares, key=lambda x: x[1], reverse=True)
    similares = similares[1:top_n+1]  # ignora o próprio café

    nome_ref = df.iloc[indice_cafe]['name']
    desc_ref = df.iloc[indice_cafe]['desc_1']
    desc_ref_pt = traduzir_texto(desc_ref)

    print("="*100)
    print(f"Café de referência:\n")
    print(f"[{indice_cafe}] Nome: {nome_ref}")
    print(f"Avaliação (PT): {desc_ref_pt}")
    print("="*100)
    print("\nRecomendações similares:\n")

    for i, score in similares:
        nome = df.iloc[i]['name']
        desc = df.iloc[i]['desc_1']
        desc_pt = traduzir_texto(desc)

        print(f"[{i}] Nome: {nome}")
        print(f"Similaridade: {score:.2f}")
        print(f"Avaliação (PT): {desc_pt}")
        print("—" * 100)


# 6. BUSCA POR NOME DO CAFÉ
def buscar_por_nome(nome_busca):
    resultados = df[df['name'].str.lower().str.contains(nome_busca.lower())]
    if resultados.empty:
        print("Nenhum café encontrado com esse nome.")
        return
    print("Cafés encontrados:")
    for idx, row in resultados.iterrows():
        print(f"[{idx}] {row['name']}")

    try:
        indice_escolhido = int(input("Digite o número (índice) do café para ver recomendações: "))
        if indice_escolhido in df.index:
            recomendar_cafes(indice_cafe=indice_escolhido, top_n=3)
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Digite apenas um número.")

# 7. EXECUÇÃO
nome_digitado = input("Digite o nome (ou parte do nome) do café que deseja buscar: ")
buscar_por_nome(nome_digitado)

