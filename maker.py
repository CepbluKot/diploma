import paho.mqtt.client as mqtt


client = mqtt.Client()
client.connect("localhost", 1883, 60)
while 1:
    import random,json
    deita = {"lat":random.randint(40,50), "lon": random.randint(40,50)}
    print(json.dumps(deita))
    
    client.publish(payload=json.dumps(deita), topic="data/gnss_str")
    import time
    time.sleep(1)
