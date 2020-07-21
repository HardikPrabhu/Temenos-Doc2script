#automating document extraction
from bs4 import BeautifulSoup
import os
import re
import pickle
mycwd = os.getcwd()
#import the configuration
os.chdir("Config")
with open ("configuration","rb") as f:
    configuration=pickle.load(f)
print(configuration)

docs={}

for m in configuration['Documents']:
 os.chdir(m)
 loc=os.getcwd()

 cleanr = re.compile('<.*?>')  # removing tags
 for k in os.listdir():
    try:
     os.chdir(k)
     docs[k]=""

     for j in os.listdir():
         with open(j) as html_file:
             soup = BeautifulSoup(html_file, "lxml")
         doc=""
         match = soup.find("div", class_="first_div")
         cleantext = re.sub(cleanr, '', str(match))
         doc = doc + cleantext
         docs[k]=docs[k]+doc
    except:
        print("not selecting introduction html")

    os.chdir(loc)

os.chdir(mycwd)
os.chdir("model")
with open("documents","wb") as f:
    pickle.dump(docs,f)


