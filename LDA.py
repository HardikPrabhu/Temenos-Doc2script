import pickle
import os
import gensim
from gensim.models.coherencemodel import CoherenceModel
import logging
import re
mycwd=os.getcwd()


# Grid of topics for evaluation
grid=[10,11,12,13,15,16,17,19,20,22,25,30]
#Number of passess for test model...the optimized model will have no. of passess less than pa
pa=150


optimize=True

if optimize==False:  #To set topics/passes manually 1. change  optimize=False(line 16) 2. set values below
    pa = 80
    topics=20

#Loading Configuration
os.chdir("Config")
with open ("configuration","rb") as f:
    configuration=pickle.load(f)

a=configuration["dir"][0]
b=configuration["dir"][1]

os.chdir(mycwd)
#Loading the inputs required for model
os.chdir("model")
with open("dictionary", "rb") as f:
    dictionary=pickle.load(f)
with open("train", "rb") as f:
    bag=pickle.load(f)
logging.basicConfig(filename='ldamodel.log', format='%(asctime)s : %(levelname)s: %(message)s', level=logging.INFO)



def evaluation_model(topics_num,m):   #input: (list of number of topics, m=number of passess)
  x=[]
  for k in topics_num:
    lda = gensim.models.LdaModel(bag, id2word=dictionary, passes=m, num_topics=k, random_state=42, iterations=1000,alpha=a, eta=b, eval_every=None)
    cm = CoherenceModel(model=lda, corpus=bag, coherence='u_mass')  #by default top words=20
    x.append([k,cm.get_coherence()])
  return x

#Testrun with arbitarily number of topics, passess(pa)
if optimize==True:
 test = gensim.models.LdaModel(bag, id2word=dictionary, passes=pa, num_topics=20, random_state=42, iterations=1000,alpha=a, eta=b, eval_every=None)



 r= re.compile("LDA training, (\d+) topics")
 p = re.compile(r"PROGRESS: pass (\d+), at document #(\d+\/\d+)")
 q=re.compile("topic diff=(\d+[.]\d+)")
 x={} #if the logfile contains multiple lda models, maintain a dic
 s=0
 #number of passess
 count=0
 with open ('ldamodel.log',"r") as f:
    for l in f:
     if s==0 and r.findall(l):
         t=r.findall(l)[0]
         x[t]=[]
         s=1
     if s==1 and p.findall(l):
         if p.findall(l)[0][1].split('/')[0] == p.findall(l)[0][1].split('/')[1]:
          s=2
     if s==2 and q.findall(l):
         x[t].append(float(q.findall(l)[0]))
         count=count+1
         s=1
     if count==pa:

         s=0
         count=0



 pass_=0
 y= x["20"]
 while pass_< pa-1 and y[pass_]>0.025:     #bound for top diff value
    pass_=pass_+1
 pass_=pass_+1

 c=evaluation_model(grid,pass_)
 topics=c[0][0]
 val=c[0][1]
 for i in c:
    if i[1]>val:
        val=i[1]
        topics=i[0]
 pa=pass_

lda = gensim.models.LdaModel(bag, id2word=dictionary, passes=pa, num_topics=topics, random_state=42, iterations=1000,alpha=a, eta=b, minimum_probability=0,eval_every=None )

for i in lda.show_topics(num_topics=topics,num_words=10):
  print(i[0],":",i[1])

#clearing log file:
with open ('ldamodel.log',"w") as f:
    pass

with open("model", "wb") as f:
      pickle.dump(lda, f)
