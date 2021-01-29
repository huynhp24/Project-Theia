import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='urlQueue')

def callbackfunc(ch, method, properties, text):
    print(" Recieved message from sender: %r" % text)

channel.basic_consume(queue='urlQueue',
                      on_message_callback=callbackfunc,
                      auto_ack=True)
print('Waiting to get messages from sender')
channel.start_consuming()