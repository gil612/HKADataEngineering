# https://www.rabbitmq.com/tutorials/tutorial-two-python.html
# start RabbitMQ with docker:
# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
# decrease default acknowledgement timeout (30 min) in docker image:
# connect to docker image (start a bash):
## docker container exec -it rabbitmq /bin/bash
# in order to decrease the timeout to 30 s, we add the following line to the rabbitmq configuration file:
## echo consumer_timeout=30000 >> /etc/rabbitmq/conf.d/10-default-guest-user.conf
# restart the docker image
## docker restart rabbitmq
##### SQL ######
# We use SQL database HKA_AMQP, table MessageFromAMQP. The table MessageFromAMQP has to columns: timestamp (datetime2) and message (nvarchar)
# For a script to create the table MessageFromAMQP, see 00-sql-query-create-table-MessageFromAMQP.sql
# python package for RabbitMQ
import pika
import time
import datetime
import random
import pyodbc

# initialize random with current system time
random.seed()
# SQL server connection
server='DESKTOP-7GQKTPR' 
database='HKA_AMQP' 
username='DESKTOP-7GQKTPR\gilbaram' 
cnxn= pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';Trusted_Connection=yes;')
cursor=cnxn.cursor()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

# AMQP ensures that all messages are delivered and processed (saved to SQL server)
def callback(ch, method, properties, body):
    print(" [x] {} Received {}".format(datetime.datetime.now(),body.decode()))
    time.sleep(body.count(b'.'))
    # acknowledge the message; make sure that the message is delivered and processed by a worker
    timestamp=datetime.datetime.now()
    # worker randomly fails
    if random.random() > 0.995:
        print('Worker failed at {}. This worker will not consume messages any more.'.format(timestamp))
    else:
        # save work to SQL database
        try:
            cursor.execute("INSERT INTO MessageFromAMQP(timestamp,message) VALUES (?,?)",timestamp,body.decode("UTF-8"))
            cnxn.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(" [x] {} Saved message {} to SQL server.".format(datetime.datetime.now(),body.decode("UTF-8")))
        except:
            print("Insert to SQL Server failed.")

# give one message to a worker at a time, i.e. don't dispatch a new message to a worker until it has processed and acknowledged the previous one
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
