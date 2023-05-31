import json
import spacy
from nltk.tokenize import TextTilingTokenizer
from nltk.corpus import stopwords
import sys
import fasttext
import ndjson

articleSegments = {}

def main():
  negacionista = False
  if len(sys.argv) > 1:
    negacionista = sys.argv[1] != 'False'
  print("Loading dataset...")
  negacionista_articles = loadDataset('dataset.ndjson',  negacionista)
  print("Applying TextTiling for segmentation...")
  negacionista_segments = segmentate(negacionista_articles)
  print("Tagging segments...")
  tags = classify(negacionista_segments)
  print("Generating ndjson file...")
  outputName = 'notNegacionistaSegmentationOutput.ndjson'
  if negacionista:
    outputName = 'negacionistaSegmentationOutput.ndjson'
  saveToFile(negacionista_articles, tags, outputName)

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
          articles.append(article)

      except:
        pass

    return articles


def segmentate(collection):
  nlp = spacy.load('es_core_news_sm')
  segmentCollection = list()

  stopwords_spanish = set(stopwords.words('spanish'))
  tt = TextTilingTokenizer(stopwords=stopwords_spanish)


  for article in collection:
    text = " ".join(article["sentencias"])
    text = "".join(text.splitlines())
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

    index = collection.index(article)
    segmentIndexes = []
    offset = len(segmentCollection)
    # Imprimimos los segmentos
    for i in range(len(ttsegments)):
      segmentCollection.append(ttsegments[i])
      segmentIndexes.append(offset + i)

    articleSegments[index] = segmentIndexes

  return segmentCollection

def classify(segments):
  clasificador = fasttext.load_model("clasificador.bin")

  tags = []
  for segment in segments:
      tag = clasificador.predict(segment.replace('\n', ''))[0][0]
      tags.append(tag)
  return tags

def saveToFile(articles, tags, outputFileName):
  with open(outputFileName,'w',encoding='utf-8') as output:
    writer = ndjson.writer(output, ensure_ascii=False)
    for article in articles:
      segments = articleSegments[articles.index(article)]
      articleTags = []
      for segment in segments:
        articleTags.append(tags[segment])
      def labelPercentage(label):
        return len(list(filter(lambda tag: (tag == label), articleTags)))/len(articleTags)
      energiasrenovables = labelPercentage('__label__energiasrenovables')
      combustibles = labelPercentage('__label__combustibles')
      emisiones = labelPercentage('__label__emisiones')
      consumohogares = labelPercentage('__label__consumohogares')
      huellacarbono = labelPercentage('__label__huellacarbono')
      cumbreclima = labelPercentage('__label__cumbreclima')
      ods = labelPercentage('__label__ods')
      article['etiquetas'] = { 
        'energiasrenovables': energiasrenovables, 
        'combustibles': combustibles,
        'emisiones': emisiones,
        'consumohogares': consumohogares,
        'huellacarbono': huellacarbono,
        'cumbreclima': cumbreclima,
        'ods': ods
        }
      writer.writerow(article)

main()