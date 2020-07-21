from tkinter import *
from tkinter import filedialog, messagebox
import os
import subprocess
import sys
import pickle
root=Tk()
root.title("Doc2script")
root.geometry("500x620+150+0")
mycwd=os.getcwd()
configuration={}
Script_loc=[]
Document_loc=[]
Scripts=0
Documents=0
Stopwords=[]
diralpha=""
direta=""
tend=""
selectfields=[1,1,0,0,0]
s=DoubleVar()
s2=DoubleVar()
map_setting={}
sim=IntVar()
threshold=DoubleVar()
#menu bar functions
def imp_script():
    global Scripts, Script_loc
    try:
     fs = filedialog.askdirectory(title="Select Folder containing scripts")
     Script_loc.append(fs)
     os.chdir(Script_loc[-1])
     k=len(os.listdir())
     Scripts=Scripts+k
     label1.config(text=f"Scripts: {Scripts}")
     status.config(text=f" {k} Scripts added",fg="green")
     os.chdir(mycwd)
    except:
        status.config(text="Try again: Error Importing scripts", fg="red")
        Script_loc=[]
def imp_doc():
    global Documents, Document_loc
    try:
     Document_loc.append(filedialog.askdirectory(title="Select Folder containing Documents"))
     os.chdir(Document_loc[-1])
     k = len(os.listdir())
     Documents = Documents + k
     label2.config(text=f"Documents: {Documents}")
     status.config(text=f" {k} Documents added", fg="green")

    except:
        status.config(text="Try again: Error Importing documents", fg="red")
        Document_loc=[]
def help1():
    subprocess.Popen(r"help/Application Architecture.pdf", shell=True)

def help2():
    subprocess.Popen(r"help/final ppt.pdf",shell=True)
def savemodel():
    global Model
    if Model=="None":
        messagebox.showerror("Error", "No Model found!")
        status.config(text="Error: Generate a model first ", fg="red")
    print("model saved")


menu=Menu(root)
imp=Menu(menu)
helpopt=Menu(menu)
root.config(menu=menu)
menu.add_cascade(label="import", menu=imp)
menu.add_cascade(label="help",menu=helpopt)
helpopt.add_command(label="Application Architecture",command=help1)
helpopt.add_command(label="How mapping is done using LDA",command=help2)
imp.add_command(label="Scripts",command=imp_script)
imp.add_command(label="Documents",command=imp_doc)
imp.add_separator()
#status bar
status=Label(root,text="Ready",bd=1,relief=SUNKEN,anchor=W,bg="white")
status.pack(side=BOTTOM,fill=X,pady=10)

#Body

Frame1=Frame(root,bg="RoyalBlue1",padx=20,pady=20)
Frame1.pack(side=TOP,fill=X)
label1=Label(Frame1,text=f"Scripts: {Scripts}",bg="RoyalBlue1",padx=10,fg="white")
label1.pack(side=LEFT)
label2=Label(Frame1,text=f"Documents: {Documents}",bg="RoyalBlue1",fg="white")
label2.pack(side=LEFT)
l=Label(Frame1,text=f"Model: None",bg="RoyalBlue1",fg="yellow",padx=10)
l.pack(side=RIGHT)
Frame2=Frame(root,pady=10)
Frame2.pack(fill=X)
conf=Label(Frame2,text="Configuration",fg="RoyalBlue2",font=("Arial", 15))
conf.pack()

#dictionary functions:
def addstopword():
    global Stopwords
    try:
      filename =filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
      with open(filename,"r") as f:
         m=f.read().split(" ")
         m.pop()
      Stopwords=Stopwords+m
      status.config(text=f"{len(m)}  stopwords added",fg="green")
      stolabel2.config(text=f"words: {len(Stopwords)}",font=("Arial",7),fg="green")
    except:
        status.config(text="Try Again: Error importing stopwords", fg="red")

def clrstp():
    global Stopwords
    Stopwords=[]
    status.config(text="Cleared user defined stopwords", fg="green")
    stolabel2.config(text=f"words: {len(Stopwords)}", font=("Arial", 7), fg="green")
#dictionary frame
Frame3=Frame(root)
Frame3.pack(fill=X)
dict=Label(Frame3,text="Dictionary settings",fg="RoyalBlue3")
dict.grid(row=1, column=0,pady=5,sticky=W)
filtex=Label(Frame3, text="1. Filter extremes:")
filtex.grid(row=2,column=0,sticky=W)
flabel1=Label(Frame3, text="Remove words with total count less than")
count=IntVar()
count.set(5)
f1=Entry(Frame3,textvariable=count)
flabel2=Label(Frame3, text="Remove words occuring over")
percent=DoubleVar()
f2=Entry(Frame3,textvariable=percent)
percent.set(60)
flabel3=Label(Frame3, text="percentage of scripts")
flabel1.grid(row=3,column=0)
f1.grid(row=3,column=1)
flabel2.grid(row=4,column=0,sticky=E)
f2.grid(row=4,column=1)
flabel3.grid(row=4,column=2)
stotex=Label(Frame3, text="2. Adding user defined Stopwords:")
stolabel=Label(Frame3,text="Add the text file(s) containing the stopwords.",font=("Arial",7),fg="green")
stolabel2=Label(Frame3,text=f"words: {len(Stopwords)}",font=("Arial",7),fg="green")
stotex.grid(row=5,column=0,sticky=W)
stolabel.grid(row=6,column=0,sticky=W, columnspan=2)
stolabel2.grid(row=6,column=2)
addstop=Button(Frame3,text="Add",command=addstopword,padx=20)
addstop.grid(row=7,column=0)
disclear=Button(Frame3,text="clear",command=clrstp,padx=20)
disclear.grid(row=7,column=2,sticky=E)

Label(Frame3,text="3. Tendency to form phrases:").grid(row=8,column=0,sticky=W)
w=Scale(Frame3,orient=HORIZONTAL,length=200, from_=0,to=40,resolution=0.001,fg="RoyalBlue3")
w.set(10)
w.grid(row=8,column=1,columnspan=2)
Label(Frame3,text="Frequent").grid(row =9,column=1,sticky=W)
Label(Frame3,text="Rare").grid(row =9,column=2,sticky=E)
Label(Frame3,text="(Bi-grams and Tri-grams)", fg="green",font=("Arial",7)).grid(row =9,column=0,sticky=N)
#Dirchlet functions
symlab=""
symval=""
def symalpa():
    global alpval, symlab,symval,s
    if alp.get()==2:
     symlab=Label(Frame4,text="set symmetric alpha (alpha >0):",fg="blue")
     symval=Entry(Frame4,textvariable=s)
     status.config(text="Set symmetric alpha (alpha >0)",fg="blue")
     symlab.grid(row=2, column=2,sticky=E)
     symval.grid(row=2, column=3)
     alpval=2
    if alp.get()==1 and alpval==2:
        symlab.destroy()
        symval.delete(0, END)
        symval.destroy()
        status.config(text="alpha=Auto",fg="blue")
        alpval=1

etasymlab=""
etasymval=""
def symeta():
    global etaval,etasymlab,etasymval,s2
    if eta.get()==2:
     etasymlab=Label(Frame4,text="set symmetric eta (eta >0):",fg="blue")
     etasymval=Entry(Frame4,textvariable=s2)
     status.config(text="Set symmetric eta (eta>0))",fg="blue")
     etasymlab.grid(row=4, column=2,sticky=E)
     etasymval.grid(row=4, column=3)
     etaval=2
    if eta.get()==1 and etaval==2:
        etasymlab.destroy()
        etasymval.delete(0, END)
        etasymval.destroy()
        status.config(text="eta=Auto",fg="blue")
        etaval=1



#Dirchlet Frame
Frame4=Frame(root,pady=5)
Frame4.pack(fill=X)
Dir=Label(Frame4,text=" Dirichlet Parameters",fg="RoyalBlue3")
Dir.grid(row=0,column=0,sticky=W)
Alpha=Label(Frame4,text="alpha")
Label(Frame4,text="Recommended alpha=auto",font=("Arial",7),fg="green").grid(row=1,column=2)
Alpha.grid(row=1,column=0)
alp=IntVar()
alp.set(1)
alpval=1
Radiobutton(Frame4, text="auto",variable=alp,value=1,command=symalpa).grid(row=2,column=0)
Radiobutton(Frame4, text="symmetric",variable=alp,value=2,command= symalpa).grid(row=2,column=1)

eta=Label(Frame4,text="eta")
Label(Frame4,text="Recommended eta=auto",font=("Arial",7),fg="green").grid(row=3,column=2)
Eta=Label(Frame4,text="eta")
Eta.grid(row=3,column=0)
eta=IntVar()
eta.set(1)
etaval=1
Radiobutton(Frame4, text="auto",variable=eta,value=1,command=symeta).grid(row=4,column=0)
Radiobutton(Frame4, text="symmetric",variable=eta,value=2,command= symeta).grid(row=4,column=1)




#Scripts func
def select_field():
   select=Tk()

   def doneselect():
       global selectfields
       select.destroy()
       selectfields=[svar1.get(),svar2.get(),svar3.get(),svar4.get(),svar5.get()]
       status.config(text="Fields selected"+str(selectfields),fg="green")
       return
   select.title("Select Fields")
   select.geometry("400x150+150+150")
   Label(select, text= " Select descriptions from the objects belonging to:").grid(row=0, column=0,columnspan=4,sticky=W)
   svar1 = IntVar(select)
   s1=Checkbutton(select, text="sstobjectList", variable=svar1,padx=2)
   s1.grid(row=1, column=0,sticky=W)
   s1.select()
   svar2 = IntVar(select)
   s2=Checkbutton(select, text="ssaobject", variable=svar2,padx=2)
   s2.grid(row=1, column=1, sticky=W)
   s2.select()
   svar3 = IntVar(select)
   Checkbutton(select, text="rfObjectList", variable=svar3,padx=2).grid(row=1, column=2, sticky=W)
   svar4=IntVar(select)
   Checkbutton(select, text="fvObjectList", variable=svar4,padx=2).grid(row=1, column=3, sticky=W)
   svar5 = IntVar(select)
   Checkbutton(select, text="ssfoObjectList", variable=svar5, padx=2).grid(row=2, column=0, sticky=W)
   Label(select, text="Text under Field names and application for objects under sstobjectList are also selected.",fg="green",font=("Arial",7)).grid(row=3, column=0, columnspan=4,sticky=W)
   Button(select,text="Done",command=doneselect,bg="RoyalBlue2",fg="white",padx=20,pady=10).grid(row=4,column=1)
   return
#Model genration button function
def genmodel():
    status.config(text="Generating Model...This might take a while.", fg="green")
    os.chdir(mycwd)
    global diralpha,s,s2, direta, percent, count,w, tend, Script_loc, Document_loc
    if Scripts == 0:
        messagebox.showerror("Error", "No Scripts found!")
        status.config(text="Error: Import scripts first", fg="red")
    else:
     try:
      tend=w.get()
      if alp.get()==1:
        diralpha="auto"
      else:
         diralpha=s.get()
      if eta.get()==1:
       direta="auto"
      else:
         direta=s2.get()
      if direta==0 or diralpha==0:
          raise Exception
      percent.get()
      count.get()
      #saving dict of config values
      configuration["Filter extremes"]=(count.get(),percent.get())
      configuration["Stopwords"]=Stopwords
      configuration["tend_phrase"]=tend
      configuration["dir"]=[diralpha, direta]
      configuration["select_field"]=selectfields
      configuration["scripts"]=Script_loc
      configuration["Documents"]=Document_loc
      os.chdir("config")
      with open ("configuration","wb") as f:
          pickle.dump(configuration,f)
      os.chdir(mycwd)
      subprocess.call([sys.executable, r"Preprocessing.py"])
      subprocess.call([sys.executable, r"LDA.py"])
      l.config(text="model: Generated" )
      status.config(text="Model is ready.",fg="green")
      mapping()

     except:
        status.config(text="Error: Some entries have invalid entry format", fg="red")


    return
#Scripts frame
Frame5=Frame(root)
Frame5.pack(fill=X)
Label(Frame5,text="Scripts settings",fg="RoyalBlue3").grid(row=0,column=0,sticky=W)
Label(Frame5,text="Select the fields from which the texts are selected:").grid(row=1,column=0)
Button(Frame5, text="SELECT",command= select_field,padx=20).grid(row=2, column=0)
Button(Frame5, text="Generate Model", fg="white",bg="Royalblue2", command=genmodel,padx=15,pady=15).grid(row =3, column=3,rowspan=2,columnspan=2,sticky=E)

def gen_map():
    global map_setting,sim,threshold
    if  Documents==0:
        messagebox.showerror("Error", "No Documents found!")
        status.config(text="Error: Import documents first", fg="red")
    else:

     configuration["Documents"]=Document_loc
     os.chdir(mycwd)
     os.chdir(r'Config')
     with open("configuration", "wb") as f:
            pickle.dump(configuration, f)
     map_setting["threshold"]=threshold.get()
     map_setting["similarity_measure"]=sim.get()
     with open("map_config", "wb") as f:
            pickle.dump(map_setting, f)
     os.chdir(mycwd)
     subprocess.call([sys.executable, r"extract_docs.py"])
     subprocess.call([sys.executable, r"Mapping.py"])
     status.config(text="Done mapping...open file mappings present in the working directory.", fg="green")
def mapping():
    Frame2.destroy()
    Frame3.destroy()
    Frame4.destroy()
    Frame5.destroy()
    map=Frame(root)
    map.pack(fill=X)
    Label(map, text="Mapping", fg="RoyalBlue2", font=("Arial", 15)).pack()
    similar=Frame(root)
    similar.pack(fill=X)
    Label(similar, text="Similarity Settings",fg="Royalblue3").grid(row=0,column=0,sticky=W)
    Label(similar,text="1. Select Similarity measure:").grid(row=1,column=0,sticky=W)
    def sm():
        global sim
        sim.get()
        return

    sim.set(1)
    Radiobutton(similar,text="Cosine similarity",variable=sim,value=1,command=sm).grid(row=2, column=0)
    Radiobutton(similar, text="Jensen Shannon Divergence", variable=sim, value=2, command=sm).grid(row=2,column=1)
    Label(similar, text="2. Set threshold:").grid(row=3, column=0, sticky=W)
    Entry(similar,textvariable=threshold, width=10).grid(row=4,column=0)
    Label(similar, text="Set a value between 0 and 1",font=("Arial", 7),fg="green").grid(row=4, column=1, sticky=W)
    Message(similar, text="Note: JSD is a measure of disimilarity. Set a low value for threshold. Scripts and documents with score less than the threshold will get mapped.",fg="blue",aspect=1000).grid(row=5, column=0,columnspan=2, sticky=W)
    mapframe = Frame(root,pady=10)
    mapframe.pack(fill=X)
    Button(mapframe,text="Generate Mapping", fg="white",bg="Royalblue2",command=gen_map,padx=20,pady=20).pack()


root.mainloop()

