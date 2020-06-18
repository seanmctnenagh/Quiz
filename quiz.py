import json
import random
import sys
import datetime
import os 
from fuzzywuzzy import fuzz

dir_path = r"C:\Users\seanm\Documents\Quiz\questions"

def args():
    practise = False
    reverse = False

    if input("Practise:(Y/N)").upper() == "Y":
        practise = True
    if input("Reverse:(Y/N)").upper() == "Y":
        reverse = True

    return practise,reverse

##############################################################################################################

def loadTopics():
    topics = []
    for root, dirs, files in os.walk(dir_path): 
        for file in files:  
            if file.endswith('.json'): 
                topics.append(file)
    return topics

##############################################################################################################

def loadTopicFile(topic,topics):
    if topic == "random":
        topic = topics[random.randrange(0,len(topics))]
    else:
        topic = topic + ".json"

    print(topic)

    with open("C:/Users/seanm/Documents/Quiz/questions/"+topic , mode='r', encoding='utf-8') as f:
        data = json.load(f)

    return data,topic

##############################################################################################################

def loadQnA(ans,qs,data,reverse):
    for x,y in data.items():
        if reverse:
            ans.append(x)
            qs.append(y)
        else:
            qs.append(x)
            ans.append(y) 
    return ans,qs

##############################################################################################################

def runQuiz(questions,answers):
    test = []
    length = int(len(questions) - 2) # Length of test (-2 for date and level)

    print(str(length)+" questions")
    print()

    correct = 0

    for i in range(0,length):
        id = random.randrange(0,length,1)
        while id in test:
            id = random.randrange(0,length,1)
        test.append(id)
        answer = input(str(i+1)+". "+str(questions[id])+"\n")
        if fuzz.token_sort_ratio(answer.upper(),answers[id].upper()) > 80:
            print("Correct\n"+answers[id]+"\n")
            correct += 1
        else:
            print("IncorrectXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"+str(answers[id])+"\n")
        correctPct = int((100*correct)/(length))
        print(str(correctPct)+"%")

    return length,correct

##############################################################################################################

def tidyUp(length, correct, data, topic, practise):
    print("You got "+ str(correct) +"/"+str(length)+" questions correct: "+str(int((100*correct)/length))+"%")

    level = int(data["level"])

    repeat = False

    if practise:
        level = data["level"]
    elif correct == length & level == 8:
        level = 8
    elif correct == length:
        level += 1
    elif (100*correct) / length > 90:
        level = level
        repeat = True
    else:
        level = 0

    data["level"] = level

    now = datetime.datetime.now() - datetime.timedelta(hours=3)

    if practise:
        date = data["date"]
    elif level == 0 or repeat:
        date = now
    elif level == 1:
        date = now + datetime.timedelta(days=1)
    elif level == 2:
        date = now + datetime.timedelta(days=3)
    elif level == 3:
        date = now + datetime.timedelta(weeks=1)
    elif level == 4:
        date = now + datetime.timedelta(weeks=2)
    elif level == 5:
        date = now + datetime.timedelta(weeks=4)
    elif level == 6:
        date = now + datetime.timedelta(weeks=8)
    elif level == 7:
        date = now + datetime.timedelta(weeks=16)
    elif level == 8:
        date = now + datetime.timedelta(weeks=32)
    if not practise:
        data["date"] = date.strftime("%x")

    with open("questions/"+topic, mode='w', encoding='utf-8') as fs:
        json.dump(data,fs,indent=4)

##############################################################################################################

def today():
    topics = loadTopics()

    print()

    for topic in topics:
        with open("questions/"+topic , mode='r', encoding='utf-8') as f:
            data = json.load(f)
            if data["date"] <= datetime.datetime.now().strftime("%x"):
                spacesa = " "*(20-len(topic))
                spacesb = " "*5
                print(topic+spacesa+data["date"]+spacesb+"level "+str(data["level"]))
        
    print()

##############################################################################################################    

def loadTopicData(topics):
    topicsData = []
    for topic in topics: # loadTopicData
        with open("questions/"+topic , mode='r', encoding='utf-8') as f:
            data = json.load(f)
            if data["level"] == "100":
                pass
            else:
                topicsData.append({
                    "topic" : topic,
                    "date" : data["date"],
                    "level" : data["level"]
                })
    return topicsData

##############################################################################################################

def view():
    sort = input("Sort by: Date / Level / Name\n").upper()
    sorts = ["DATE","LEVEL","NAME"]

    if sort not in sorts:
        view()

    
    topics = loadTopics()
    topicsData = loadTopicData(topics)
    print()

    if len(sys.argv)>1:
        sort = sys.argv[1]
        if sort =="LEVEL":
            topicsData = sorted(topicsData, key = lambda i: str(i["level"]))
        elif sort =="DATE":
            topicsData = sorted(topicsData, key = lambda i: str(i["date"]),reverse=True)
        elif sort =="NAME":
            topicsData = sorted(topicsData, key = lambda i: str(i["topic"]))

    print()

    for topicDate in topicsData:
        spacesa = " "*(20-len(topicDate["topic"]))
        spacesb = " "*5
        print(topicDate["topic"]+spacesa+topicDate["date"]+spacesb+"level "+str(topicDate["level"]))

###################################################################################################################

def quiz():
    questions = [] # List of questions
    answers = [] # List of answers

    topic = input("Topic:") # Get topic

    practise,reverse = args() # Set reverse and practise bools

    topics = loadTopics() # Load qna to data and topic name to topic

    data,topic = loadTopicFile(topic,topics)

    answers,questions = loadQnA(answers,questions,data,reverse) # Fill questions and answers lists

    length,correct = runQuiz(questions,answers) # Run Quiz

    tidyUp(length, correct, data, topic, practise) 


##############################################################################################################
run = False

if input("\n\n\n\n\n\nStart program?(Y/N)").upper() == "Y":
    run = True

while(run):
    task = input("Today, View or Quiz?\n").upper()

    if task == "TODAY":
        today()
    elif task == "VIEW":
        view()
    elif task == "QUIZ":
        quiz()