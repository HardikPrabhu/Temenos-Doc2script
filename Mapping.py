import pickle
import os
import gensim
from gensim.parsing import strip_tags, strip_punctuation, strip_multiple_whitespaces, remove_stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
from numpy import dot
from numpy.linalg import norm
mycwd=os.getcwd()

#import configuration
os.chdir("Config")
with open("map_config", "rb") as f:
    map_setting=pickle.load(f)
os.chdir(mycwd)
#import the topic model
os.chdir(r"model")
with open("model", "rb") as f:
    lda=pickle.load(f)
#import the model inputs
with open("dictionary", "rb") as f:
 dictionary=pickle.load(f)
with open("train", "rb") as f:
 bag=pickle.load(f)

#import the dict containing scripts
with open("script_dict", "rb") as f:
  script_dict=pickle.load(f)

#import the phraser
with open("phrases", "rb") as f:
  phrases=pickle.load(f)


CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation,strip_multiple_whitespaces,remove_stopwords]
lemmatizer = WordNetLemmatizer()

# function to allocate topic distribution to a text
def allocate_topic(string):
  vector = gensim.parsing.preprocessing.preprocess_string(string, CUSTOM_FILTERS)
  vector = phrases[vector]
  vector = [lemmatizer.lemmatize(x,pos="n") for x in vector]
  vector = [lemmatizer.lemmatize(x,pos="v") for x in vector]
  vector = dictionary.doc2bow(vector)

  return  lda[vector]

document_dist={}
#allocating topic distributions to documentations
with open("documents", "rb") as f:
  documents=pickle.load(f)

for j in documents:
  document_dist[j]=allocate_topic(documents[j])


#allocating topic distribution to scripts
script_dist={}
for j in script_dict:
  script_dist[j]=allocate_topic(script_dict[j])





doc_vectors={}
for i in document_dist:
    doc_vectors[i]=[]
    for j in document_dist[i]:
        doc_vectors[i].append(j[1])

script_vectors={}
for i in script_dist:
    script_vectors[i]=[]
    for j in script_dist[i]:
        script_vectors[i].append(j[1])

def cosine(a,b):
    return  dot(a,b)/(norm(a)*norm(b))

threshold=map_setting["threshold"]
mapping=""
if map_setting["similarity_measure"]==1:
 #list of (doc,script,score)
 doc_script_score=[]
 for i in doc_vectors:
      for j in script_vectors:

        doc_script_score.append((i,j,cosine(doc_vectors[i],script_vectors[j])))
 doc_script_score = sorted(doc_script_score, key=lambda x: x[2],reverse=True)


 #mapping

 mapping1={}
 for i in doc_script_score:
    if i[0] in mapping1:
        if i[2] >= threshold:
            mapping1[i[0]].append(i[1])
    else:
        if i[2] >=threshold:
            mapping1[i[0]]=[i[1]]
 mapping=mapping1


if  map_setting["similarity_measure"]==2:

 #mapping2
 import scipy.stats
 def jensen_shannon_distance(p, q):
    """
    method to compute the Jenson-Shannon Distance
    between two probability distributions
    """

    # convert the vectors into numpy arrays
    p = np.array(p)
    q = np.array(q)

    # calculate m
    m = (p + q) / 2

    # compute Jensen Shannon Divergence
    divergence = (scipy.stats.entropy(p, m) + scipy.stats.entropy(q, m)) / 2

    # compute the Jensen Shannon Distance, sqrt of divergence
    distance = np.sqrt(divergence)

    return distance

 doc_script_score2=[]
 for i in doc_vectors:
      for j in script_vectors:

        doc_script_score2.append((i,j,jensen_shannon_distance(doc_vectors[i],script_vectors[j])))
 doc_script_score2 = sorted(doc_script_score2, key=lambda x: x[2])
 threshold=0.35
 mapping2={}
 for i in doc_script_score2:
    if i[0] in mapping2:
        if i[2] < threshold:
            mapping2[i[0]].append(i[1])
    else:
        if i[2] <threshold:
            mapping2[i[0]]=[i[1]]
 mapping=mapping2



#To see what scripts are mapped to given document.
def see_scripts(doc,map):
    for i in map[doc]:
        print(script_dict[i][:150])





#How close the documents are to each other.(using cosine)
doc_sim={}
for i in doc_vectors:
    for j in doc_vectors:
        if i!=j:
            doc_sim[str(set([i,j]))]=[cosine(doc_vectors[i],doc_vectors[j])]


k=[3,10]
x=[[a[0],k[1]*a[1]] for a in lda.show_topic(k[0])]


def words(doc,m):
 y=[]
 for k in document_dist[doc]:
  x=[[a[0],k[1]*a[1]] for a in lda.show_topic(k[0],topn=int(len(dictionary)/10))]
  for j in x:
    found=0
    for i in y:
        if i[0]==j[0]:
            i[1]=i[1]+j[1]
            found=1
            break
    if found==0:
        y.append(j)
 return [a[0] for a in sorted(y,key=lambda x:x[1],reverse=True)[:m]]



os.chdir(mycwd)
os.chdir("mappings")
with open ("Doc2script mapping","w") as f:
    f.write(str(mapping))

with open("Topwords for documents","w") as f:
    for j in document_dist:
        f.write(str(j)+":"+str(words(j,60))+"\n\n\n")


