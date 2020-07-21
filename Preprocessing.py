import pickle
import json
import os
import gensim
from gensim.parsing import strip_tags, strip_punctuation, strip_multiple_whitespaces, remove_stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models.phrases import Phrases


mycwd = os.getcwd()
#import the configuration
os.chdir("Config")
with open ("configuration","rb") as f:
    configuration=pickle.load(f)


Scripts={} # maintain the scripts as dictionary indexed by scenerio id.

#Load the scripts by using the location given in configuration:
for k in configuration["scripts"]:
 os.chdir(k)


 for j in os.listdir():
  with open(j,"r") as f:
    cont=f.read()
    data = json.loads(cont)
    if configuration["select_field"][1]==1:
     Scripts[data["scenarioId"]]=data["ssaObject"]["description"]
    x = data['sstObjectList']
    for i in x:
            z=""
            for k in i["fieldDefinition"]:
                z=z+" "+ k["fieldName"]
            Scripts[data["scenarioId"]] = Scripts[data["scenarioId"]] + " " + i["application"] + " " + z
            if configuration["select_field"][0]==1:
              Scripts[data["scenarioId"]]=Scripts[data["scenarioId"]]+" "+ i["description"]

    if configuration["select_field"][3]==1:
        x= data["fvObjectList"]
        for i in x:
            z=""
            z=z+" "+i["description"]

        Scripts[data["scenarioId"]] = Scripts[data["scenarioId"]] + z

    if configuration["select_field"][2]==1:
        x= data["rfObjectList"]
        for i in x:
            z=""
            z=z+" "+i["description"]

        Scripts[data["scenarioId"]] = Scripts[data["scenarioId"]] + z

    if configuration["select_field"][4]==1:
        x= data["ssfoObjectList"]
        for i in x:
            z=""
            z=z+" "+i["description"]

        Scripts[data["scenarioId"]] = Scripts[data["scenarioId"]] + z

#Going back to project directory
os.chdir(mycwd)

#Catching references
ref={}
for j in Scripts:
    words=Scripts[j].replace(".", " ")
    words=words.split()
    for i in words:
        if i in Scripts and i!=j:  #ignore the self reference
                 if i in ref:
                   ref[i].append(j)
                 else:
                     ref[i]=[j]
                 if j in ref:
                    ref[j].append(i)
                 else:
                    ref[j] = [i]


collection=[]
final=[]
for i in ref:
    ref[i].append(i)
    collection.append(set(ref[i]))
while collection:
 w=1
 while w !=len(collection):
    if collection[0] & collection[w]:
        collection[0]=collection[0].union(collection.pop(w))
    else:
        w=w+1

 final.append(collection.pop(0))  #final is a collection of related scripts


text_corpus=[]
marked=[]
for j in final:
    y=""
    for script in j:
     y= y + Scripts[script]
     marked.append(script)
    text_corpus.append(y)            #create a text corpus for further preprocessing
    for script in j:
      Scripts[script]=y                  #modify the payments dictionary

for i in Scripts:
    if i not in marked:
        text_corpus.append(Scripts[i])

#converting to bag of words
CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation,strip_multiple_whitespaces,remove_stopwords]
def preprocessing():
  for i in text_corpus:
    doc=[]
    document=gensim.parsing.preprocessing.preprocess_string(i,CUSTOM_FILTERS)
    remove = ["create", "script", "scenario"]+configuration["Stopwords"] #filtering user defined stopwords
    for i in document:
        if i not in remove and len(i)>1:
            doc.append(i)
    yield doc

#To model bigrams, we need to feed list of list of words or a genrator, such as preprocessing().
bigram = Phrases(preprocessing(),threshold=configuration["tend_phrase"])
bigram_token = []
for sent in preprocessing():
    bigram_token.append(bigram[sent])
# If we apply Phrases again on bigram, we can extract trigrams and possibly 4-grams.
phrases= Phrases(bigram_token,threshold=configuration["tend_phrase"])
phrases_token = []
for sent in preprocessing():
    phrases_token.append(phrases[sent])


#Lemmatzing
texts=[]
lemmatizer = WordNetLemmatizer()
for doc in phrases_token:
   for i in range(len(doc)):
      doc[i]= lemmatizer.lemmatize(doc[i].lower(),pos="n" )
      doc[i] = lemmatizer.lemmatize(doc[i].lower(), pos="v")
   texts.append(doc)



dictionary=gensim.corpora.Dictionary(texts)
#filtering extremes of dictionary
dictionary.filter_extremes(no_below=configuration["Filter extremes"][0], no_above=configuration["Filter extremes"][1]*0.1)
bag = [dictionary.doc2bow(tokens) for tokens in texts]
#saving dictionary
os.chdir(mycwd)
os.chdir(r"model")
with open("dictionary", "wb") as f:
   pickle.dump(dictionary,f)
#saving the collection of set of dependent scripts
with open("collection","wb") as f:
    pickle.dump(final, f)
#saving payment_dict
with open("script_dict","wb") as f:
    pickle.dump(Scripts, f)
#saving Training corpus
with open("Train","wb") as f:
    pickle.dump(bag, f)
#saving phrases
with open("phrases","wb") as f:
    pickle.dump(phrases,f)



