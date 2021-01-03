import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='urlQueue')

channel.basic_publish(exchange='',
                      routing_key='urlQueue',
                      body='RabbitMQ test')
print(" Sent a queue")
connection.close()