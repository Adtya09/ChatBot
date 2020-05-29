from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import time



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
trainer.train('chatterbot.corpus.siya.training_files')
print("Training Started")
s=input("ques")
res=str(chatbot.generate_response(s));
print(res)
chatbot.g
a=[]
chatbot.generate_response()