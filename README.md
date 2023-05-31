# Ejercicio de minería de textos - Web Semántica - MIW - Curso 2022/23
## Autora: Carmen Rendueles Martínez - UO269689

*Contenidos*
- [Introducción](#introduccion)
- [Datasets](#datasets)
- [Requisitos previos](#requisitos-previos)


### Introducción
Este es el repositorio utilizado para el almacenamiento y documentación del ejercicio de minería de textos realizado por Carmen Rendueles Martínez. Este ejercicio pertenece a la asignatura Web Semántica, del Máster en Ingeniería Web de la Universidad de Oviedo.


En los próximos apartados, se detallará primero toda la información y contexto previo a la programación y, después, se detallará el desarrollo de las diferentes partes del ejercicio y, por lo tanto, todos los archivos incluidos en este repositorio acabarán siendo detallados.



### Datasets
Para la realización de este ejercicio, se nos aportaba un dataset inicial que incluía noticias clasificadas como relacionadas con el cambio climático. Este dataset se encuentra en el archivo `dataset.ndjson`.


Se nos indicaba que para hacer los ejercicios se debería separar este dataset en noticias 'negacionistas' y 'no negacionistas' y utilizar uno u otro en función de la última cifra de nuestro DNI. Al ser la última cifra de mi DNI par, me tocaría utilizar la siguiente división:
- Apartados 1 a 6 con noticias 'negacionistas'
- Apartados 7 a 8 con noticias 'NO negacionistas'


Para aplicar esta separación, cuando se carga el dataset, se hace una comprobación que selecciona únicamente los documentos que cumplen con la condición correspondiente, siendo en cada caso:

- Negacionistas: `len(article['sentencias_disagree']) > len(article['sentencias_NOT_disagree'])`
- No negacionistas: `len(article['sentencias_disagree']) <= len(article['sentencias_NOT_disagree'])`


### Requisitos previos
Para poder ejecutar todos los archivos sin problemas, se deberán instalar y descargar una serie de librerías y colecciones de datos.
Para ello, se deberán ejecutar los siguientes comandos:
- `pip install simhash`
- `pip install spacy`
- `python -m spacy download es_core_news_sm`
- `pip install nltk`
- `python import nltk`
- `python nltk.download("stopwords")`
- `pip install sklearn`
- `pip install textacy`
- `pip install fasttext`
- `pip install fasttext-wheel`
- `pip install ndjson`