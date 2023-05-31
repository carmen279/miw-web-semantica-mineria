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

num_clusters = 50

clustering = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=1000, n_init=1, verbose=True)
clustering.fit(doc_term_matrix)

clustered_docs = dict()
docs_per_cluster = dict()

with open('clusteringOutput.txt', 'w', encoding='utf-8') as output:

    for i in range(len(clustering.labels_)):
        try:
            clustered_docs[clustering.labels_[i]].append(i)
            docs_per_cluster[clustering.labels_[i]]+=1
        except:
            clustered_docs[clustering.labels_[i]] = list()
            clustered_docs[clustering.labels_[i]].append(i)
            docs_per_cluster[clustering.labels_[i]]=1

    ids = list(docs_per_cluster.keys())
    ids.sort()
    sorted_docs_per_cluster = {i: docs_per_cluster[i] for i in ids}

    terminos = vectorizador.get_feature_names_out()

    indice_cluster_terminos = clustering.cluster_centers_.argsort()[:, ::-1]

    for cluster_id in sorted_docs_per_cluster:

        output.write("Cluster %d (%d documentos): " % (cluster_id, docs_per_cluster[cluster_id]))

        for term_id in indice_cluster_terminos[cluster_id, :10]:

            if clustering.cluster_centers_[cluster_id][term_id]!=0:
                output.write('"%s",' % terminos[term_id])
            
        output.write('\n\n')

        ejemplares = clustered_docs[cluster_id]
        random.shuffle(ejemplares)
        for ejemplar in ejemplares[0:5]:
            output.write("\t"+segments[ejemplar][0:140].replace('\n','')+"...\n")
        output.write('\n\n\n')