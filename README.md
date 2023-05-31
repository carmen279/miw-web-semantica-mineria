# Ejercicio de minería de textos - Web Semántica - MIW - Curso 2022/23
## Autora: Carmen Rendueles Martínez - UO269689

*Contenidos*:
- [Introducción](#introducción)
- [Datasets](#datasets)
- [Requisitos previos](#requisitos-previos)
- [Apartado 1](#apartados-1-y-2)
- [Apartado 3](#apartado-3)
- [Apartado 4](#apartado-4)
- [Apartado 5](#apartado-5)
- [Apartado 6](#apartado-6)
- [Apartados 7 y 8](#apartados-7-y-8)


### Introducción
Este es el repositorio utilizado para el almacenamiento y documentación del [ejercicio de minería de textos](https://docs.google.com/document/d/1thbS1u3uhpGunz6iJh-bYmNkzQ7KWumyqI9UJf0DRis/edit#) realizado por Carmen Rendueles Martínez. Este ejercicio pertenece a la asignatura Web Semántica, del Máster en Ingeniería Web de la Universidad de Oviedo.


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
De aquí en adelante, se supondrá que estas dependencias se encuentran instaladas.

### Apartados 1 y 2
El código para los apartados 1 y 2 se ofrece en el archivo `segmentation.py`.


Para la ejecución de este archivo sólo será necesario ejecutarlo en línea de comandos con `python .\segmentation.py`. Cabe destacar, que este código por defecto se ejecuta con el dataset asignado, pero se puede ejecutar con el contrario con `python .\segmentation.py False`.


Este archivo contiene métodos con los diferentes procesos solicitados en los apartados 1 y 2. Estos métodos son los siguientes:
- `loadDataset`: Este método carga el dataset solicitado a memoria.
- `removeDuplications`: Este método busca y elimina artículos cuasiduplicados, utilizando para ello SimHash.
- `segmentate`: Este método procesa un listado de textos y realiza las siguientes acciones:
    - Segmenta la noticia en sentencias usando spaCy.
    - Une esas sentencias en un único texto separando las sentencias con `\n\n`.
    - Usa TextTiling sobre el texto obtenido para obtener segmentos temáticamente coherentes.
    - Añade todos los segmentos a una lista única.
- `saveToFile`: Por último, este método guarda el resultado en un archivo, en este caso, al trabajar con textos negacionistas, llamado `negacionistaSegmentationOutput.json`. Este archivo se puede obtener ejecutando el programa pero se ofrece ya en el repositorio.

### Apartado 3
El código relativo al apartado 3 se ofrece en el archivo `clustering.py`.


En este archivo se lee el resultado de los apartados anteriores y, a partir de esta lista de segmentos, se vectorizan y se aplica el algoritmo de clusterización K-means con 50 clusters. Después, se procesa el resultado y se guarda en un nuevo archivo, llamado `clusteringOutput.txt`.


Para la ejecución de este archivo sólo será necesario ejecutarlo en línea de comandos con `python .\clustering.py`. 

*¡IMPORTANTE!* el resultado cambia en cada ejecución y, por lo tanto, es importante tener cuidado para no sobreescribir los resultados que se deseen conservar.

### Apartado 4
Este apartado, no incluye código al requerir únicamente un proceso manual. 


El resultado de este ejercicio se ofrece en el archivo `clusteringOutput-selection.txt`. Este archivo contiene la selección de los 7 clústers que aparentaban más interesantes de los generados tras la ejecución del apartado anterior. A cada uno de estos clusters se les asigna una etiqueta que parezca agregar adecuadamente las palabras ofrecidas por el clúster.

### Apartado 5


### Apartado 6


### Apartados 7 y 8