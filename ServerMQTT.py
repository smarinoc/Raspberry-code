import paho.mqtt.client as mqtt
broker_address = "127.0.0.1"
client = mqtt.Client()
	
def publish(topic, message):
    client.publish(topic,message)
    
def build(subMessage):       
    def on_message(client, userdata, message):
        subMessage(message)
    global client    
    client = mqtt.Client(client_id='p1',clean_session = True)
    client.connect(broker_address)
    client.on_message = on_message
    client.loop_start()
    print("Subscribing to a topic")
    client.subscribe("voting/identify/cam")
    client.subscribe("voting/identify/fingerprint")
    client.subscribe("voting/state")
    client.subscribe("voting/enable")
    client.subscribe("voting/onVoting")
