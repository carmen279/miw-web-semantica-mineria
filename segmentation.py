import json
from simhash import Simhash, SimhashIndex
import spacy
from nltk.tokenize import TextTilingTokenizer
from nltk.corpus import stopwords
import sys


def main():
  negacionista = True
  if len(sys.argv) > 1:
    negacionista = sys.argv[1] != 'False'
  print("Loading dataset...")
  negacionista_articles = loadDataset('dataset.ndjson',  negacionista)
  print("Removing duplicated articles...")
  negacionista_articles = removeDuplications(negacionista_articles)
  print("Applying TextTiling for segmentation...")
  negacionista_segments = segmentate(negacionista_articles)
  print("Saving output in JSON file...")
  outputName = 'notNegacionistaSegmentationOutput.json'
  if negacionista:
    outputName = 'negacionistaSegmentationOutput.json'
  saveToFile(negacionista_segments, outputName)

def loadDataset(fileName, negacionistas = True):
  with open(fileName, 'r', encoding='utf-8', errors='ignore') as dataset:
    lines = dataset.readlines()
    articles = list()

    for line in lines:
      try:
        article = json.loads(line)
        condition = len(article['sentencias_disagree']) > len(article['sentencias_NOT_disagree'])
        if not negacionistas:
          condition = not condition

        if condition:
          text = " ".join(article["sentencias"])
          text = "".join(text.splitlines())
          articles.append(text)

      except:
        pass

    return articles
  
def removeDuplications(collection):
  f_value = 128
  
  cleanedCollection = []
  trashCollection = []

  signatures = []

  for i in range(len(collection)):
    signature = Simhash(collection[i], f=f_value)
    signatures.append((i, signature))

  index = SimhashIndex(signatures, k=10, f=f_value)

  for i in range(len(collection)):
    if str(i) not in trashCollection:
      signature = signatures[i][1]
      duplicated = index.get_near_dups(signature)

      if len(duplicated) == 1:
        cleanedCollection.append(collection[i])
        trashCollection.append(i)
      else:
        cleanedCollection.append(collection[int(duplicated[0])])
        for j in duplicated:
          trashCollection.append(j)

  print('Removed ' + str(len(collection) - len(cleanedCollection)) + ' quasiduplicated articles')
  return cleanedCollection

def segmentate(collection):
  nlp = spacy.load('es_core_news_sm')
  segmentCollection = list()

  stopwords_spanish = set(stopwords.words('spanish'))
  tt = TextTilingTokenizer(stopwords=stopwords_spanish)


  for text in collection:
    doc = nlp(text)
    segments = list(doc.sents)
    for i in range(len(segments)):
      segments[i] = segments[i].text

    joinedSegments = "\n\n".join(segments)

    if len(segments) == 1:
      joinedSegments += "\n\n"

    try:
      # Segmentamos el texto utilizando el algoritmo TextTiling
      ttsegments = tt.tokenize(joinedSegments)
    except:
      ttsegments = []
      ttsegments.append(joinedSegments)

    # Imprimimos los segmentos
    for i in range(len(ttsegments)):
      segmentCollection.append(ttsegments[i])

  return segmentCollection

def saveToFile(collection, outputFileName):
  with open(outputFileName,'w',encoding='utf-8') as output:
    jsonfile = json.dumps(collection, ensure_ascii=False)
    output.write(jsonfile)

main()