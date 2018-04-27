import os
import json

import arrow
import click
import paho.mqtt.client as mqtt

@cli.command()
def run()
    mqttc = mqtt.Client()
    mqttc.subscribe('')
