#!/usr/bin/python3

import boto3
import json
import sys
import argparse

parser=argparse.ArgumentParser(
    description='''Script to manage ec2 instance ''')
parser.add_argument('--start', action="store_true", help='start instance')
parser.add_argument('--stop', action="store_true", help='stop instance')
parser.add_argument('--status', action="store_true", help='status instance')

args=parser.parse_args()

with open("instances.conf") as json_data_file:
    data = json.load(json_data_file)

client = boto3.client('ec2')
instance_id=data["instance"]["id"]
response = client.describe_instance_status(InstanceIds=[instance_id])

instance_status = response["InstanceStatuses"]

estado=""

def main():
    global estado
    if len(sys.argv) == 2:
        config()
        action = sys.argv[1]
        estado = status()
        if action == "--start" and estado == "parada":
            start()
        elif action == "--stop" and estado == "encendida":
            stop()
        elif action == "--status":
            sys.exit(0)
        else:
            print ("La instancia ya estaba en ese estado")
    
    elif len(sys.argv) == 1:
        config()
        status()
    else:
        print ("Numero de argumentos incorrecto")
        sys.exit(1)

def config():
    with open("instances.conf") as json_data_file:
        data = json.load(json_data_file)

    client = boto3.client('ec2')
    instance_id=data["instance"]["id"]
    response = client.describe_instance_status(InstanceIds=[instance_id])

    instance_status = response["InstanceStatuses"]

def start():
    if estado == "parada":
        client.start_instances(InstanceIds=[instance_id])
        print ("-- Se ha iniciado la instancia")
    else:
        print ("-- La instancia ya estaba arrancada")

def stop():
    if estado == "encendida":
        client.stop_instances(InstanceIds=[instance_id])
        print ("-- Se ha parado la instancia")
    else:
        print ("-- La instancia ya estaba parada")

def status():
    if not instance_status:
        print ("-- La instancia esta parada")
        return "parada"
    else:
        state = response["InstanceStatuses"][0]["InstanceState"]["Name"]
        if state == 'running':
            print ("-- La instancia esta running")
            return "encendida"
        else:
            print ("Estado desconocido")

main()

