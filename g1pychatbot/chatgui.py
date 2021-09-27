import nltk
import requests
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
##import Tkinter as tk
##from PIL import ImageTk, Image, ImageEnhance

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            urlnk = random.choice(i['urls'])
            imggrp = random.choice(i['imgs'])
            break
    return result,urlnk,imggrp;

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res, urls, imgs = getResponse(ints, intents)
    return res, urls, imgs;

#Creating GUI with tkinter
import tkinter
from tkinter import *
#from tkinter import filedialog
import webbrowser
from tkinter.font import Font, nametofont
#pillow
from PIL import Image, ImageTk
from datetime import datetime

#current_time = datetime.now().strftime("%D - %H:%M \n")
current_time = datetime.now().strftime("%d %b,%Y, %H:%M %p")
# Binding events must be passed event

def show_hand_cursor(event):
    ChatLog.config(cursor='arrow')
def show_xterm_cursor(event):
    ChatLog.config(cursor='xterm')
def click(event):
    webbrowser.open('www.google.com')

def add_image(imge):
    global my_image
    #Add Image
    my_image = tkinter.PhotoImage(file=imge)
    image = Image.open(imge)
    #image = Image.open(imge).resize((150, 150), Image.ANTIALIAS)
    posn  = ChatLog.index(INSERT)

    #ChatLog.image_create(posn, image = my_image)
    ChatLog.window_create(END, window=Label(ChatLog,image=my_image,bg="lightblue",fg="#000000",width=294,anchor="nw")) # Example 2
    #ChatLog.config(bg="white", width=300, height=10)

#Define a callback function
def callback():
    url="https://margcompusoft.com/marg-price-list.html"
    webbrowser.open_new_tab(url)

def pricing():
    ChatLog.config(state=NORMAL)
    resp_ = "Pricing?"
    ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
    wraplength=300, font=("Verdana", 10), bg="#DDDDDD", bd=4, justify="left"))
    ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
    ChatLog.config(fg="grey", font=("Helvetica", 8))
    resp_ = "https://margcompusoft.com/marg-price-list.html"
    ChatLog.window_create(END, window=Button(ChatLog, fg="blue", text=resp_, width="45", height=2,
                            wraplength=280, font=("Verdana", 8,'underline'), bg="lightblue", bd=0,
                            cursor="arrow", justify="right", command= callback) )
    ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
    ChatLog.config(fg="grey", font=("Helvetica", 8))
    ChatLog.insert(END, '\n\n\n ', "right")
    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)

def margerp():
    ChatLog.config(state=NORMAL)
    resp_ = "What is Marg ERP?"
    ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
    wraplength=300, font=("Verdana", 10), bg="#DDDDDD", bd=4, justify="left"))
    ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
    ChatLog.config(fg="grey", font=("Helvetica", 8))
    resp_ ="MARG ERP 9+ is an on-premise ERP solution used by small, midsize and enterprise businesses. It offers different modules customized to the needs of retailers, distributors and manufacturers in a variety of industries."
    ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
    wraplength=300, font=("Verdana", 10), bg="lightblue", bd=1, justify="left"))
    ChatLog.insert(END, '\n'+''+'\n',"left")
    ChatLog.config(fg="grey", font=("Helvetica", 8))
    resp_ ="For more information, visit at www.margerp.com"
    ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
    wraplength=300, font=("Verdana", 10), bg="lightblue", bd=4, justify="left"))
    ChatLog.insert(END,'\n'+current_time+'\n\n',"left")
    ChatLog.config(fg="grey", font=("Helvetica", 8))
    ChatLog.insert(END, '\n\n\n ', "right")
    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)

def newuser():
    ChatLog.config(state=NORMAL)
    resp_ = "New User"
    reqclr = '#%02x%02x%02x' % (94, 104, 254)  # set your favourite rgb color
    ChatLog.insert(END, '\n\n\n ', "right")
    ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
    wraplength=300, font=("Verdana", 10), bg="#DDDDDD", bd=4, justify="left"))
    ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
    ChatLog.config(fg="grey", font=("Helvetica", 8))
    resp_ = "Thanks for showing interest in Marg Software. Please select your inquiry type."
    ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
    wraplength=300, font=("Verdana", 10), bg="lightblue", bd=4, justify="left"))
    ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
    ChatLog.config(fg="grey", font=("Helvetica", 8))
    ChatLog.insert(END, "   "+'\t')
    ChatLog.window_create(END, window=Button(ChatLog, fg="blue", text="What is Marg Erp ?", width="18", height=2,
                            wraplength=125, font=("Verdana", 8), activeforeground="white",activebackground="#EE82EE",
                            bg="white", bd=1, cursor="arrow", justify="right", command= margerp) )
    ChatLog.insert(END, "     "+'\t')
    ChatLog.window_create(END, window=Button(ChatLog, fg="blue", text="Pricing", width="14", height=2,
                            wraplength=55, font=("Verdana", 8), activeforeground="white",activebackground="#EE82EE",
                            bg="white", bd=1, cursor="arrow", justify="right", command= pricing ))
    ChatLog.insert(END, '\n\n\n ', "right")
    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)

def existuser():
    ChatLog.config(state=NORMAL)
    resp_ = "Existing User"
    reqclr = '#%02x%02x%02x' % (94, 104, 254)  # set your favourite rgb color
    ChatLog.insert(END, '\n\n\n ', "right")
    ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
    wraplength=300, font=("Verdana", 10), bg="#DDDDDD", bd=4, justify="left"))
    ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
    ChatLog.config(fg="grey", font=("Helvetica", 8))
    ChatLog.insert(END, "   "+'\t')
    ChatLog.window_create(END, window=Button(ChatLog, fg="blue", text="Registration", width="14", height=2,
                            wraplength=75, font=("Verdana", 8), activeforeground="white",activebackground="#EE82EE",
                            bg="white", bd=1, cursor="arrow", justify="right", command= newuser) )
    ChatLog.insert(END, "     "+'\t')
    ChatLog.window_create(END, window=Button(ChatLog, fg="blue", text="Licence Verification", width="18", height=2,
                            wraplength=125, font=("Verdana", 8), activeforeground="white",activebackground="#EE82EE",
                            bg="white", bd=1, cursor="arrow", justify="right", command= existuser ))
    ChatLog.insert(END, '\n\n\n ', "right")
    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)

def ucallback():
    url = "www.bizinwiz.com"
    webbrowser.open_new(url)


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    # We could change the "end" argument of the get method to be the "end-1c"
    #if we don’t want the newline in the returned input.
    #"end-1c" means the position is one character ahead of "end".
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END,"  "+"\n\n")
        msg_ = "You: " + msg+' '
        ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=msg_,
        wraplength=200, font=("Arial", 10), bg="#DDDDDD", bd=4, justify="left"))
        ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
        ChatLog.config(fg="grey", font=("Helvetica", 8))
        ChatLog.config(foreground="#0000CC", font=("Helvetica", 9))
        #ChatLog.yview(END)
        rwcl=ChatLog.index("end")
        res, urls, imgs = chatbot_response(msg)
        resp_ = "Margun: " + res +' '
        if imgs != '':
            add_image(imgs)
            ChatLog.insert(END,"  "+"\n")

        if urls != '' and urls in res:
            lstt=res.find(urls)
            lslen=len(urls)
            rw=float(rwcl)-1
            rw=rw+(lstt+9)/100
            cl=float(rwcl)-1
            cl=cl+((lstt+9+lslen)/100)
            #resp_ = "https://margcompusoft.com/marg-price-list.html"
            ChatLog.window_create(END, window=Button(ChatLog, fg="#000000", text=resp_,
                                    wraplength=300, font=("Verdana", 10), bg="lightblue", bd=0,
                                    cursor="arrow", justify="left", command= ucallback) )

            #label = Text(ChatLog,  fg="#000000", text=resp_,
            #wraplength=300, font=("Verdana", 10), bg="lightblue", bd=4, justify="left")
            #ChatLog.window_create(END, label)


            ChatLog.tag_add("link", rw, cl)
            ChatLog.tag_config('link', foreground='blue', underline=True)

            ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
            ChatLog.config(fg="grey", font=("Helvetica", 8))

        else:
            ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
            wraplength=300, font=("Verdana", 10), bg="lightblue", bd=4, justify="left"))
            ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
            ChatLog.config(fg="grey", font=("Helvetica", 8))


            #ucallback("http://www.ecosia.org")

            #link2 = Label(ChatLog, text="Ecosia Hyperlink", fg="blue", cursor="arrow")
            #link2.pack()
            #link2.bind("<Button-1>", lambda e: ucallback("http://www.ecosia.org"))

            ##ChatLog.tag_add("link", rw, cl)
            ##ChatLog.tag_config('link', foreground='blue', underline=True)
            # Mouse pointer
            ##ChatLog.tag_bind('link', '<Enter>', show_hand_cursor)
            # Mouse leaves
            ##ChatLog.tag_bind('link', '<Leave>', show_xterm_cursor)
            # Left click
            ##ChatLog.tag_bind('link', '<Button-1>', click)
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

base = Tk()
base.title(string='Marg Chatbot')
base.iconbitmap("ask-marg.ico")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)


w = Canvas(base, width=700, height=500)
w.pack()
#w.create_rectangle(50, 20, 150, 80, fill="#476042")

mycolor = '#%02x%02x%02x' % (64, 204, 208)  # set your favourite rgb color
#base.attributes('-topmost', 0)
#p1 = PhotoImage(file = '123.png')
#base.iconphoto(True, p1)
#base.overrideredirect(1)
#base.attributes('-toolwindow', True)
#Label(base, text= "Ask Marg", font=('Helvetica bold',20), fg= "green").pack(pady=20)

frame = Label(text='Ask-Marg',
    fg="green",
    font=("Verdana",13,'bold')
)
frame.pack(expand=True, fill=BOTH)

frameb = Label(text='Developed by MARG',
    fg="grey",
    font=("Verdana",7,'bold')
)
frameb.pack(expand=True, fill=BOTH)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="10", width="50", font="Arial")
ChatLog.config(state=DISABLED)
#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="arrow")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",7,'bold'), text="Developed by MARG",wraplength=77, width="12", height=5,
                    bd=0, activebackground="#3c9d9b",fg="green", command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="#fffff0",width="69", height="6", fg='#000000', font=("Arial",11,''))

#EntryBox.bind("<Return>", send)
EntryBox.bind("<Return>", (lambda event: send()))

#Activate the focus
EntryBox.focus_set()
EntryBox.pack()

#Initialisation ChatLog
ChatLog.config(state=NORMAL)
resp_ = "Hi! I am a Bot, Your virtual assistant"
ChatLog.insert(END, '\n ', "right")
ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
wraplength=300, font=("Verdana", 10), bg="lightblue", bd=4, justify="left"))
ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
ChatLog.config(fg="grey", font=("Helvetica", 8))
resp_ = "Happy to help you explore some interesting things! How about starting with one of the below ones?"
ChatLog.window_create(END, window=Label(ChatLog, fg="#000000", text=resp_,
wraplength=300, font=("Verdana", 10), bg="lightblue", bd=4, justify="left"))
ChatLog.window_create(END, window=Label(ChatLog, fg="#ff0f00", text="👇",
wraplength=10, font=("Verdana", 15), bg="white", bd=4, justify="left"))
ChatLog.insert(END, '\n'+current_time+'\n\n',"left")
ChatLog.config(fg="grey", font=("Helvetica", 8))

ChatLog.insert(END, "   "+'\t')
ChatLog.window_create(END, window=Button(ChatLog, fg="blue", text="New User", width="10", height=2,
                        wraplength=55, font=("Verdana", 8), activeforeground="white",activebackground="#EE82EE",
                        bg="white", bd=1, cursor="arrow", justify="right", command= newuser) )
ChatLog.insert(END, "     "+'\t')
ChatLog.window_create(END, window=Button(ChatLog, fg="blue", text="Existing User", width="14", height=2,
                        wraplength=75, font=("Verdana", 8), activeforeground="white",activebackground="#EE82EE",
                        bg="white", bd=1, cursor="arrow", justify="right", command= existuser ))
ChatLog.insert(END, '\n'+" "+'\n\n',"left")
ChatLog.config(fg="grey", font=("Helvetica", 8))

ChatLog.config(state=DISABLED)
ChatLog.yview(END)

#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=7,y=27, height=365, width=369)
frame.place(x=2,y=3,height=20,width=123)
frameb.place(x=125,y=392,height=20,width=375)
EntryBox.place(x=6, y=415, height=60, width=386)
SendButton.place(x=0, y=-1, height=0)

#w.create_line(clm1, row1, clm2, row2, fill="#476042", width=1)
w.create_line(0, 413, 400, 413, fill="#476042", width=1)
base.mainloop()
