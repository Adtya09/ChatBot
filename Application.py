# import statements
from flask import Flask, render_template, request
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer



app=Flask(__name__)

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

##Comment below

#trainer.train('chatterbot.corpus.training.Version_1')
def writeToFileQ(data):
    file = open(
        'C:\\Users\\AmitJ\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\chatterbot_corpus\\data\\training\\Q2A.yml',
        'a')
    file.write(data)
    file.close()


# function to write 'Questions Answered' to a file for Evaluation.
def writeToFileA(data):
    file = open(
        'C:\\Users\\AmitJ\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\chatterbot_corpus\\data\\training\\A2Q.yml',
        'a')
    file.write(data)
    file.close()


@app.route("/")
def chatWindow():
    #return render_template("chatbox.html")
    return render_template("test.html")
@app.route("/getResponse")
def getresponse():
    ques=request.args.get("msg")
    bot_response=str(chatbot.get_response(ques))
    if ("|" in str(bot_response)):
        temp = str(bot_response).replace("|", "<br>")
        bot_response=temp
    if str(bot_response) == "Sorry ,I did not get you !!.":
        writeToFileQ("- - " + ques + "\n")
        writeToFileQ("  - " + "\n")

    else:
        writeToFileA("- - " + ques + "\n")
        writeToFileA("  - " + str(bot_response) + "\n")

    return bot_response



if __name__ =='__main__':
    app.run()






