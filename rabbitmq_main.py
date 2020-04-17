import pika
import json
import os
import id_scripts.id_card
import cv2
import boto3
import logging
import sys

def callback(channel, method_frame, header_frame, body):
    result = None
    try:
        data = json.loads(body)

        s3_client.download_file(bucket_name, data['image'], data['image'])

        validate_fields = {}
        if data["name"] is not None:
            validate_fields['name'] = data["name"].strip()
        if data["birthdate"] is not None:
            validate_fields['birthdate'] = data["birthdate"]
        if data["mothername"] is not None:
            validate_fields['mother_name'] = data["mothername"]
        if data["releasedate"] is not None:
            validate_fields['release_date'] = data["releasedate"]
        if data["id_num"] is not None:
            validate_fields['id_number'] = data["id_num"]
        if data["birthplace"] is not None:
            validate_fields['birthplace'] = data["birthplace"]

        img = cv2.imread(data['image'])
        card = id_scripts.id_card.validate_id_card(img, 0, validate_fields)

        if card['validation_failed']:
            result = 'reject'
        elif card['validation_success']:
            result = 'accept'
        else:
            result = 'validate'
    except Exception as e:
        result = None
        channel.basic_nack(delivery_tag=method_frame.delivery_tag)
        logging.exception(e)
    finally:
        try:
            os.remove(data['image'])
        except:
            result = result


    if result is not None:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        channel.basic_publish(exchange='',
                          routing_key='taxid.result.queue',
                          body='{'
                               '"uuid":' + str(data["uuid"]) + ','
                               '"result":"' + result + '"}')

if __name__ == "__main__":

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    if os.environ.get('VCAP_SERVICES') != None:
        data = json.loads(os.environ.get('VCAP_SERVICES'))
    else:
        #with open("taxid-reader-vcap-sample.json") as file:
        #    data = json.load(file)
        logging.error("Enviroment variable 'VCAP_SERVICES' not found!")
        quit(-1)

    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        aws_access_key_id=data['cloud-object-storage'][0]['credentials']['cos_hmac_keys']['access_key_id'],
        aws_secret_access_key=data['cloud-object-storage'][0]['credentials']['cos_hmac_keys']['secret_access_key'],
        endpoint_url=data['user-provided'][0]['credentials']['cos_url'],
    )
    bucket_name = data['user-provided'][0]['credentials']['bucket_name']

    connection = pika.BlockingConnection(pika.ConnectionParameters(data["compose-for-rabbitmq"][0]["credentials"]["uri"]))
    channel = connection.channel()

    channel.queue_declare(queue='taxid.in.queue')
    channel.queue_declare(queue='taxid.result.queue')

    channel.basic_consume(callback,
                          queue='taxid.in.queue',
                          no_ack=False)

    channel.start_consuming()

