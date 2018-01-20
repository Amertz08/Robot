import os
import json

import click
import paho.mqtt.publish as publish

BROKER_PORT = os.getenv('BROKER_PORT') or 1883

@click.group()
def cli():
    pass


@cli.command()
def test():
    data = {
        'device_id': '1',
        'message': 'HHELLOO'
    }
    publish.single('blah/blah', json.dumps(data),
        hostname='broker', port=int(BROKER_PORT))


if __name__ == '__main__':
    cli()
