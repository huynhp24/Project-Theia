#!/usr/bin/env python

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='uploads')
channel.queue_declare(queue='grab_result')
channel.basic_publish(exchange='',
        routing_key='uploads',
        body='https://www.justonecookbook.com/wp-content/uploads/2018/12/Shabu-Shabu-I-2.jpg')

print(" ---Sent to RabbitMQ---")

connection.close()
