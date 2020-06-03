# import statements
from itertools import dropwhile
from netrc import netrc

from flask import Flask, render_template, request,session
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import time
from chatterbot.logic import  BestMatch
from numpy import finfo

app=Flask(__name__)
app.secret_key = "super secret key"
chatbot = ChatBot(
    'Dug Dug',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Sorry ,I did not get you !!.'
        }
    ],
    database_uri='mongodb://localhost:27017/induction_Main_t2'
    , preprocessors=['chatterbot.preprocessors.clean_whitespace'], read_Only=False)

##### It is used to drop the  existing database .
#chatbot.storage.drop()

########trainer is used to train the chatbot for first time.

trainer = ChatterBotCorpusTrainer(chatbot)
print("Training Started")


USER_QUES=""
count=0
alternateResp = ["Amit"]
Size=0
##Comment below

#trainer.train('chatterbot.corpus.siya.training_files')

def writeToFileQues(ques):
    file = open(
        'C:\\Users\\AmitJ\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\chatterbot_corpus\\data\\siya\\training_files\\training_online.yml',
        'a')
    temp= '- - '
    temp=temp+ques
    file.write(temp)
    file.close()

def writeToFileAns(ans):
    file = open(
        'C:\\Users\\AmitJ\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\chatterbot_corpus\\data\\siya\\training_files\\training_online.yml',
        'a')
    temp= '  - '
    temp=temp+ans
    file.write(temp)
    file.close()


def writeToFileQ(data):
    file = open(
        'C:\\Users\\AmitJ\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\chatterbot_corpus\\data\\siya\\evaluation\\Q2A.yml',
        'a')
    file.write(data)
    file.close()


# function to write 'Questions Answered' to a file for Evaluation.
def writeToFileA(data):
    file = open(
        'C:\\Users\\AmitJ\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\chatterbot_corpus\\data\\siya\\evaluation\\A2Q.yml',
        'a')
    file.write(data)
    file.close()

def matchedResponses(ques):
    getAllResp = str([BestMatch.allResponse])
    getAllResp = getAllResp.replace("[", " ")
    getAllResp = getAllResp.replace("]", " ")
    getAllResp = getAllResp.replace("<", " ")
    getAllResp = getAllResp.strip(" ")
    # print("After \n"+ a)
    # getAllResp=getAllResp+','
    tempGA = getAllResp.split('>,')
    # print(tempGA)
    global alternateResp
    alternateResp.clear()
    k = 1
    for i in tempGA:
        s = i[i.index(":") + 1:len(i)]
        if (k == len(tempGA)):
            s = s[:len(s) - 1]

        k = k + 1
        alternateResp.append(s)


    global Size ,count
    count=0
    Size=0
    tempSet=set(alternateResp)
    alternateResp=list(tempSet)

    #print(alternateResp)


@app.route("/")
def chatWindow():
    return render_template("Siya_UI.html")
@app.route("/getResponse")
def getresponse():

    ques=request.args.get("msg")
    ques=str(ques).lower()
    USER_QUES=ques
    bot_response=str(chatbot.get_response(ques))


    if bot_response != 'Sorry ,I did not get you !!.':
        if alternateResp:
            matchedResponses(USER_QUES)
            print("Altres main :",alternateResp)


    if ("|" in str(bot_response)):
        temp = str(bot_response).replace("|", "<br>")
        bot_response=temp
    if str(bot_response) == "Sorry ,I did not get you !!.":
        writeToFileQ("- - " + ques + "\n")
        writeToFileQ("  - " + "\n")

    else:
        writeToFileA("- - " + ques + "\n")
        writeToFileA("  - " + str(bot_response) + "\n")

    time.sleep(1)
    return bot_response

@app.route("/dislike")
def dislikedResponse():
    req=request.args.get("wrongRes")
    global  alternateResp
    global count
    global Size
    nextResponse =""
    print('Req='+req)
    print(alternateResp)
    for i in range(count,len(alternateResp)):
        print(count)
        if(req==alternateResp[i]):
            count+=1
            continue

        else:
            nextResponse=alternateResp[count]
            count += 1
            break

    if(Size>=len(alternateResp)):
        nextResponse="Apologies for the wrong info !!..<br>&nbsp&nbsp&nbsp&nbsp&nbsp I am Still Learning.."
    Size += 1
    if ("|" in str(nextResponse)):
        temp = str(nextResponse).replace("|", "<br>")
        nextResponse=temp
    print('Next='+ nextResponse)
    time.sleep(1)
    return nextResponse

@app.route("/validateLogin" ,methods=["POST","GET"])
def validateLogin():
    if request.method == "POST":
        print("In validate  login")
        user = request.form.get("username")
        user = str(user).lower()
        password = request.form.get("pass")
        print(user,password)
        if( user=="trainer1" and password=="trainer1234"):
            session['username'] = request.args.get("username")
            if 'username' in session:
                return render_template("Siya_Training.html")
            else:
                return render_template("login.html")
        else:
            return render_template("login.html",data="error")

    if request.method == "GET":
        return render_template("login.html")



@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/writeQuestion")
def writeQues():
    ques=request.args.get("ques")
    writeToFileQues(ques)
    return "ok"


@app.route("/writeAnswer")
def writeAnswer():
    ans = request.args.get("ans")
    writeToFileAns(ans)
    return "ok"




if __name__ =='__main__':
    app.run(debug=True)




