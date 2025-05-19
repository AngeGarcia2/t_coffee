# -*- coding: utf-8 -*-
"""
Created on Sun May 18 22:49:26 2025

@author: User
"""


# 1. IMPORTAÇÃO DE BIBLIOTECAS
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator

# 2. DOWNLOAD DE RECURSOS NLTK (apenas uma vez)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# 3. FUNÇÃO DE PRÉ-PROCESSAMENTO
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = nltk.word_tokenize(text.lower()) 
    tokens = [t for t in tokens if t not in string.punctuation]  
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]  
    return ' '.join(tokens)

# 4. CARREGAMENTO DO DATASET
caminho = r"C:\Users\User\Desktop\t_algebra\coffee_analysis.csv"
df = pd.read_csv(caminho)

# 5. PRÉ-PROCESSAMENTO DOS TEXTOS
df['texto_tratado'] = df['desc_1'].apply(preprocess_text)

# 6. VETORIZAÇÃO TF-IDF
vetorizador = TfidfVectorizer()
matriz_tfidf = vetorizador.fit_transform(df['texto_tratado'])

# 7. CÁLCULO DA SIMILARIDADE
cosine_sim = cosine_similarity(matriz_tfidf, matriz_tfidf)

# 8. FUNÇÃO DE RECOMENDAÇÃO
def recomendar_cafes(indice_cafe, top_n=5):
    similares = list(enumerate(cosine_sim[indice_cafe]))
    similares = sorted(similares, key=lambda x: x[1], reverse=True)[1:top_n+1]

    print("="*100)
    print(f"Café de referência:\n")
    print(f"[{indice_cafe}] Nome: {df.iloc[indice_cafe]['name']}")
    print("Avaliação (em português):")
    print(traduzir_texto(df.iloc[indice_cafe]['desc_1']))
    print("="*100)
    print("\nRecomendações similares:\n")

    for i, score in similares:
        nome = df.iloc[i]['name']
        desc = df.iloc[i]['desc_1']
        traducao = traduzir_texto(desc)
        print(f"[{i}] Nome: {nome}")
        print(f"Similaridade: {score:.2f}")
        print(f"Avaliação (em português): {traducao}")
        print("—" * 100)

# 9. TRADUÇÃO
def traduzir_texto(texto):
    tradutor = Translator()
    try:
        traducao = tradutor.translate(texto, src='en', dest='pt')
        return traducao.text
    except Exception:
        return texto 

# 10. BUSCA POR NOME
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

# 11. EXECUÇÃO
nome_digitado = input("Digite o nome (ou parte do nome) do café que deseja buscar: ")
buscar_por_nome(nome_digitado)
