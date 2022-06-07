from neuralintents import GenericAssistant

chatbot = GenericAssistant("intents.json")
chatbot.train_model()
chatbot.save_model()
while True:
    print(chatbot.request(input("enter message: ")))
