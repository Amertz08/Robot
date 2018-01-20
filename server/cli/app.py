import json

import click
import paho.mqtt.publish as publish

@click.group()
def cli():
    pass


@cli.command()
def test():
    data = {
        'device_id': '1',
        'message': 'HHELLOO'
    }
    publish.single('blah/blah', json.dumps(data), hostname='broker')


if __name__ == '__main__':
    cli()
