import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json','r')as f:
    intents=json.load(f)
    
FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]

all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name="vits info bot"

def get_response(msg):
    sentence = tokenize(msg)
    x = bag_of_words(sentence,all_words)
    x = x.reshape(1,x.shape[0])
    x = torch.from_numpy(x)
    
    output=model(x)
    _, predicted=torch.max(output,dim=1)
    tag=tags[predicted.item()]
    
    probs = torch.softmax(output,dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item()>0.75:
        for intent in intents["intents"]:
           if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I do not understand. please contact college for more details..."

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

    
# print("Let's chat! type '0' to exit")
# while True:
#     sentence=input("You: ")
#     if sentence=="0":
#         break
#     sentence = tokenize(sentence)
#     x = bag_of_words(sentence,all_words)
#     x = x.reshape(1,x.shape[0])
#     x = torch.from_numpy(x)
    
#     output=model(x)
#     _, predicted=torch.max(output,dim=1)
#     tag=tags[predicted.item()]
    
#     probs = torch.softmax(output,dim=1)
#     prob = probs[0][predicted.item()]
    
#     if prob.item()>0.75:
#         for intent in intents["intents"]:
#            if tag == intent["tag"]:
#                 print(f"{bot_name}: {random.choice(intent['responses'])}")
#     else:
#         print(f"{bot_name}: I do not understand. please contact college for more details...")


