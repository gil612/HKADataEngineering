# https://www.rabbitmq.com/tutorials/tutorial-one-python.html
# start RabbitMQ with docker:
# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
# python package for RabbitMQ
import pika, sys, os

def main():
    connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel=connection.channel()

    channel.queue_declare(queue='hello')

    # callback function to receive the messages
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # set callback function for queue 'hello'
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
