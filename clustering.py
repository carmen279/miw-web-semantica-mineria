import json
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import random

segments = []

with open('segmentationOutput.json','r',encoding='utf-8') as jsonFile:
    segments = json.load(jsonFile)

nlp = spacy.load("es_core_news_sm")
stop_words = list(spacy.lang.es.stop_words.STOP_WORDS)

vectorizador = TfidfVectorizer(encoding="utf-8", lowercase=True,
                               stop_words=stop_words, ngram_range=(1,3), 
                               max_features=10000)

doc_term_matrix = vectorizador.fit_transform(segments)

# El número de clusters debe fijarse de antemano
#
num_clusters = 50

clustering1 = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=1000, n_init=1, verbose=True)

# Se aplica el algoritmo seleccionado a la matriz que representa el corpus
#
clustering1.fit(doc_term_matrix)

# En el atributo labels_ tenemos el cluster al que pertenece cada documento.
# Usando un Counter podemos contar cuántos documentos hay por cluster.

clustered_docs1 = dict()
docs_per_cluster1 = dict()

with open('clusteringOutput.txt', 'w', encoding='utf-8') as output:

    for i in range(len(clustering1.labels_)):
        try:
            clustered_docs1[clustering1.labels_[i]].append(i)
            docs_per_cluster1[clustering1.labels_[i]]+=1
        except:
            clustered_docs1[clustering1.labels_[i]] = list()
            clustered_docs1[clustering1.labels_[i]].append(i)
            docs_per_cluster1[clustering1.labels_[i]]=1

    ids = list(docs_per_cluster1.keys())
    ids.sort()
    sorted_docs_per_cluster1 = {i: docs_per_cluster1[i] for i in ids}

    # De este modo obtenemos de nuevo el texto asociado a los términos (recordemos 
    # que con el vectorizador obtenemos una "traducción" totalmente numérica de los
    # documentos).

    terminos = vectorizador.get_feature_names_out()

    # El atributo cluster_centers_ es un array n-dimensional (realmente bidimensional)
    # que contiene el centroide de cada cluster en una matriz de clusters x términos
    # definido por pesos flotantes obviamente
    #
    # El método argsort de numpy *no* ordena el array, retorna *otro* array de las
    # mismas dimensiones que contiene *índices* en el orden en que deberían estar
    # para que los *valores* del array (en este caso cluster_centers_) estuviera 
    # ordenado
    #
    #cluster_centers = .toarray()

    indice_cluster_terminos1 = clustering1.cluster_centers_.argsort()[:, ::-1]

    # Mostramos como mucho los 10 términos más representativos de cada cluster
    for cluster_id in sorted_docs_per_cluster1:

        output.write("Cluster %d (%d documentos): " % (cluster_id, docs_per_cluster1[cluster_id]))

        for term_id in indice_cluster_terminos1[cluster_id, :10]:
            # ¡Atención! El centro son coordenadas y dichas coordenadas son términos ya
            # que trabajamos con texto y, en consecuencia, aparecen todos los términos
            # del vocabulario... Un término solo nos interesará entonces si su valor
            # no es nulo.

            if clustering1.cluster_centers_[cluster_id][term_id]!=0:
                output.write('"%s",' % terminos[term_id])
            
        output.write('\n\n')

        ejemplares = clustered_docs1[cluster_id]
        random.shuffle(ejemplares)
        for ejemplar in ejemplares[0:5]:
            output.write("\t"+segments[ejemplar][0:140].replace('\n','')+"...\n")
        output.write('\n\n\n')