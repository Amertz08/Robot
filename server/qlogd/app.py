import os
import sys
import json
import pprint

import paho.mqtt.client as mqtt

BROKER_PORT = os.getenv('BROKER_PORT') or 1883

def on_connect(client, userdata, flags, rc):
    '''On connection callback'''
    print(f'Connected with code: {rc}')
    client.subscribe('#')

def on_disconnect(client, userdata, rc):
    pass

def on_publish(client, userdata, mid):
    pass

def on_subscribe(client, userdata, mid, granted_qos):
    pass

def on_unsubscribe(client, userdata, mid):
    pass

def on_log(client, userdata, level, buf):
    pass

def on_message(client, userdata, msg):
    '''On message callback'''
    data = json.loads(msg.payload)
    print(f'Message recieved topic: {msg.topic}')
    pprint.pprint(data)


def main():
    '''Main loop'''
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect('broker', int(BROKER_PORT), 60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit()

if __name__ == '__main__':
    main()
