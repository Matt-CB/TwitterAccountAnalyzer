import os
import csv
import openai 
import random
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import Counter
import nltk
from transformers import pipeline
from mtranslate import translate
import pandas as pd
import streamlit as st
from PIL import Image
import time
                        #Para actualizar las librerias de requirements.txt en caso de error, escribir esto en consola: pip install --upgrade -r requirements.txt
load_dotenv()
st.sidebar.title("Configuración")
OPENAI_API_KEY = st.sidebar.text_input("API KEY:")
st.write("Ingresa los datos ")
IDIOMAS = ['Alemán', 'Español', 'Francés', 'Inglés', 'Italiano']
idioma = st.sidebar.selectbox("Idioma:", IDIOMAS)




class AnalizadorTwitter:
    def __init__(self):
        self.TWEETS_DIR = 'tweets'
        nltk.download('averaged_perceptron_tagger')
        nltk.download('stopwords')

    def generar_tweets(self, usuario:str, num_tweets:int=10, max_tokens:int=50, aleatoriedad:float=1):
        openai.api_key = OPENAI_API_KEY
        os.makedirs(self.TWEETS_DIR, exist_ok=True)
        archivo_csv = os.path.join(self.TWEETS_DIR, f"{usuario}_tweets.csv")
        archivo_existente = os.path.exists(archivo_csv)

        temas = ["Deportes", "Entretenimiento", "Política", "Tecnología", "Moda y belleza", "Viajes", "Negocios y finanzas", "Redes sociales e internet", "Comida y restaurantes", "Música", "Arte y cultura", "Ciencia y naturaleza", "Educación", "Videojuegos", "Humor y memes", "Tecnología e innovación", "Hogar y diseño de interiores", "Relaciones y citas", "Espiritualidad y religión", "Mascotas y animales"]
        emociones = ["Felicidad", "Tristeza", "Emoción", "Miedo", "Amor", "Asombro", "Enojo", "Sorpresa", "Diversión", "Paz"]

        tema = random.choice(temas)
        print(idioma, tema)

        with open(archivo_csv, 'a', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)

            if not archivo_existente:
                writer.writerow(['user', 'tweet'])

            for i in range(num_tweets):
                emocion = random.choice(emociones)
                prompt = f"Generar un tweet corto #{i+1} centrado en el tema de {tema}. El tweet debe expresar una emoción de {emocion} con una intensidad alta y que se noten las palabras expresivas hacia ese sentimiento, pero sin dejar de ser realista. Debe ser redactado si o si todo en {idioma}, que sea nivel nativo de {idioma}. Evita incluir emojis en el contenido del tweet. Asegúrate de que el tweet esté completamente en {idioma}, y que las emociones y los sentimientos reflejen la intensidad solicitada antes de proporcionar la respuesta."

                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=aleatoriedad,
                    n=1,
                    stop=None,
                )

                tweet = response.choices[0].text.strip()

                writer.writerow([usuario, tweet])

    def identificar_tema_principal(self, dataframe, idioma):
        tweets = dataframe['tweet'].tolist()
         # Seleccionar stopwords según el idioma
        if idioma == "Alemán":
            stop_words = set(stopwords.words('german'))
        elif idioma == "Español":
            stop_words = set(stopwords.words('spanish'))
        elif idioma == "Francés":
            stop_words = set(stopwords.words('french'))
        elif idioma == "Inglés":
            stop_words = set(stopwords.words('english'))
        elif idioma == "Italiano":
            stop_words = set(stopwords.words('italian'))
        else:
            raise ValueError("Idioma no soportado")

        # Tokenización de palabras y eliminación de stopwords
        palabras = [word for tweet in tweets for word in word_tokenize(tweet.lower()) if word.isalpha() and word not in stop_words]

        # Etiquetado de partes del discurso
        tagged_words = pos_tag(palabras)

        # Contar la frecuencia de cada palabra
        frecuencia_palabras = Counter(tagged_words)

        # Ordenar las palabras por frecuencia
        palabras_ordenadas = sorted(frecuencia_palabras.items(), key=lambda x: x[1], reverse=True)

        # Obtener el tema principal como la palabra más frecuente con etiqueta de sustantivo
        tema_principal = None
        for palabra, frecuencia in palabras_ordenadas:
            if 'NN' in palabra[1]:  # Verificar si la palabra tiene etiqueta de sustantivo
                tema_principal = palabra[0]
                break

        return tema_principal

    def traducir_columna(self, df, idioma):
        df_traducido = df.copy()
        if idioma == 'inglés':
            return df_traducido
        else:
            df_traducido['tweet_ingles'] = df_traducido['tweet'].apply(lambda x: translate(x, 'en'))
            return df_traducido

    def agregar_columna_emociones(self, df, idioma):
        clasificador = pipeline("text-classification", model="thoriqfy/indobert-emotion-classification")
        emociones_detectadas = []
        if idioma != 'inglés':
            data = self.traducir_columna(df, idioma)
            for texto in data['tweet_ingles']:
                outputs = clasificador(texto)
                emocion = outputs[0]['label']
                emociones_detectadas.append(emocion)
        else:
            data = df
            for texto in data['tweet']:
                outputs = clasificador(texto)
                emocion = outputs[0]['label']
                emociones_detectadas.append(emocion)
        data['emocion_detectada'] = emociones_detectadas

        #menciona todas las columnas de data


        return data

    
    @staticmethod
    def obtener_sentimiento(score):
        if score < 0.4:
            return 'Negativo'
        elif score < 0.6:
            return 'Neutro'
        else:
            return 'Positivo'

        
    def identificar_sentimiento(self, dataframe, idioma):
        modelo = ''
        if idioma.lower() == "alemán".lower():
            modelo = "oliverguhr/german-sentiment-bert"
        elif idioma.lower() == "español".lower():
            modelo = "dccuchile/bert-base-spanish-wwm-uncased"
        elif idioma.lower() == "francés".lower():
            modelo = "nlptown/bert-base-multilingual-uncased-sentiment"
        elif idioma.lower() == "inglés".lower():
            modelo = "bert-base-uncased"
        elif idioma.lower() == "italiano".lower():
            modelo = "Musixmatch/umberto-commoncrawl-cased-v1"

        clasificador_sentimiento = pipeline("sentiment-analysis", model=modelo)
        sentimientos = []
        for texto in dataframe['tweet']:
            resultado = clasificador_sentimiento(texto)
            etiqueta = resultado[0]['label']
            score = resultado[0]['score']
            sentimiento = self.obtener_sentimiento(score)
            sentimientos.append(sentimiento)
        dataframe['sentimiento'] = sentimientos
        return dataframe
            

def main():

    column1, column2 = st.columns([1.5, 1])
    column1.markdown("<h1 style='text-align: left; color: white;'>Análisis de <span style='color: #1DA1F2;'>Twitter</span></h1>", unsafe_allow_html=True)
    column2.image("images/Logo_of_Twitter.png", width=100)


    usuario = st.sidebar.text_input("Nombre de usuario:", "usuario_ejemplo")
    st.sidebar.markdown('<p style="font-size:12px;color:#1DA1F2;">No dejar espacios en el nombre y apellido</p>', unsafe_allow_html=True)
    st.sidebar.title('Configuración de parametros para el generador de tweets')
    num_tweets = st.sidebar.number_input("Número de tweets:", 1, 100, 10)
    st.sidebar.markdown('<p style="font-size:12px;color:#1DA1F2;">Colocar como min 5 tweets</p>', unsafe_allow_html=True) #
    max_tokens = st.sidebar.number_input("Máximo de tokens:", 1, 100, 50)
    aleatoriedad = st.sidebar.slider("Aleatoriedad:", 0.0, 1.0, 1.0)
    #idioma = st.sidebar.selectbox("Idioma:", IDIOMAS)
    tema = None
    sentimientos = ["Todos", "Positivo", "Neutro", "Negativo"]
    sentimiento = st.sidebar.selectbox("Sentimientos:", sentimientos)
    analizador = AnalizadorTwitter()
    if st.sidebar.button("Analizar"):
        with st.spinner("Generando tweets..."):
            analizador.generar_tweets(usuario, num_tweets, max_tokens, aleatoriedad)
        with st.spinner("Identificando tema principal..."):
            archivo_csv = os.path.join(analizador.TWEETS_DIR, f"{usuario}_tweets.csv")
            df = pd.read_csv(archivo_csv)
            tema = analizador.identificar_tema_principal(df, idioma)
        with st.spinner("Traduciendo tweets (si es necesario)..."):
            df_traducido = analizador.traducir_columna(df, idioma)
        with st.spinner("Detectando sentimientos..."):
            df_sentimiento = analizador.identificar_sentimiento(df, idioma)
        with st.spinner("Detectando emociones..."):
            df_emociones = analizador.agregar_columna_emociones(df_traducido, idioma)
        st.write("Cuenta: ", usuario)
        st.write("Tema principal: ", tema)
        st.write("Tabla de sentimientos:")
        st.dataframe(df_sentimiento)
        st.write("Tabla de emociones:")
        st.dataframe(df_emociones)
        st.markdown("# Tweets:")
        for i in df_emociones.index:
            row_emocion = df_emociones.loc[i]
            row_sentimiento = df_sentimiento.loc[i]
            if sentimiento == "Todos" or row_sentimiento["sentimiento"] == sentimiento:
                st.write(usuario, ':', row_emocion["tweet"])
                st.write("Emoción detectada: ", row_emocion["emocion_detectada"], f"- Sentimiento detectado: {row_sentimiento['sentimiento']}")


if __name__ == "__main__":
    main()

