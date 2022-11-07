import threading
import ServerMQTT
import JoystickAndButton

state= False

voters=[
    {"name": "Santiago",
     "id": "1",
     "voted": "False"
        },{"name": "Carlos",
     "id": "2",
     "voted": "False"
        }]

def onButton():
    if state==True:
        ServerMQTT.publish(topic="voting/enable", message="0")
        ServerMQTT.publish(topic="voting/state", message="0")
        ServerMQTT.publish(topic="voting/alert", message="1")


def validate():
    return state

global state
state= True
global voter
hilo1= threading.Thread(target=JoystickAndButton.loop, args=(onButton, validate))
hilo1.start()
    
def findVoterByName(name):
    for i in voters:
        if i["name"]==name:
            if i["voted"]=="True":
                return -1
            i["voted"]="True"
            return i["id"]
    return -1
        
def findVoterById(id):
    for i in voters:
        if i["id"]==id:
            if i["voted"]=="True":
                return -1
            i["voted"]="True"
            return i["id"]
    return -1

def subMessage(message):
    messageText=message.payload.decode("utf-8")
    if message.topic=="voting/identify/cam":
        if not messageText == "Unknown":
            voter = findVoterByName(messageText)
            ServerMQTT.publish(topic="voting/enableVoting", message="1")
            global state
            state= True
        else:
            ServerMQTT.publish(topic="voting/alert", message="0")
        ServerMQTT.publish(topic="voting/enable", message="1")
        ServerMQTT.publish(topic="voting/state", message="1")
    elif message.topic=="voting/identify/fingerprint":
        if not messageText == "unknown":
            voter = messageText
            ServerMQTT.publish(topic="voting/enableVoting", message="1")
            global state
            state= True
        else:
            ServerMQTT.publish(topic="voting/alert", message="0")
        ServerMQTT.publish(topic="voting/enable", message="1")
        ServerMQTT.publish(topic="voting/state", message="1") 
    elif message.topic=="voting/enable":
        if messageText=="0" and state==False:
            ServerMQTT.publish(topic="voting/state", message="0")
            ServerMQTT.publish(topic="voting/alert", message="1")
    elif message.topic=="voting/onVoting":
        print("llego")
        print(state)
        if state==True:
            ServerMQTT.publish(topic="raspberry/vote", message="{\"voter\":{\"id\": %i}, \"candidate\": {\"id\": %i}}") % (voter ,messageText)
            onVoting()
            
            



def onVoting():
    global state
    state= False
    ServerMQTT.publish(topic="voting/enableVoting", message="0")   
    
ServerMQTT.build(subMessage=subMessage)

while True:
    pass


