from flask import Flask, render_template, Response
from pykafka import KafkaClient
from flask_cors import CORS
import subprocess
import time
import os

def get_kafka_client():
    return KafkaClient(hosts="127.0.0.1:9092")

app = Flask(__name__)
CORS(app)



# function to start all 4 kafka services subsenquently
def start_kafka(topic_name):

    # start kafka zookeeper
    subprocess.Popen(["C:\\kafka\\bin\\windows\\zookeeper-server-start.bat", "C:\\kafka\\config\\zookeeper.properties"])
    time.sleep(5)


    # start kafka server
    subprocess.Popen(["C:\\kafka\\bin\\windows\\kafka-server-start.bat", "C:\\kafka\\config\\server.properties"])
    time.sleep(5)


    # create topic
    subprocess.Popen(["C:\\kafka\\bin\\windows\\kafka-topics.bat",
                      "--bootstrap-server",
                      "localhost:9092",
                      "--create",
                      "--topic",
                      topic_name,
                      "--partitions", "1",
                      "--replication-factor", "1"])
    time.sleep(5)


    # start producer
    subprocess.Popen([f"C:\\kafka\\bin\\windows\\kafka-console-producer.bat",
                      "--broker-list",
                       "localhost:9092",
                       "--topic",
                       topic_name])
    time.sleep(5)

    # start consumer
    subprocess.Popen([f"C:\\kafka\\bin\\windows\\kafka-console-consumer.bat",
                      "--bootstrap-server",
                      "localhost:9092",
                      "--topic",
                      topic_name,
                      "--from-beginning"])
    time.sleep(5) 
    


@app.route("/")
def index():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script's directory
    file_path = os.path.join(script_dir, "truck1.py") 

    subprocess.Popen(["python", file_path])

    return(render_template("index.html"))


# Consumer API
@app.route("/topic/<topicname>")
def get_messages(topicname):
    client = get_kafka_client()
    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield "data:{0}\n\n".format(i.value.decode())
    return Response(events(), mimetype = "text/event-stream")



if __name__ == "__main__":
    topic_name = f"topic-{int(time.time())}"    # it creates a new topic name for every session
    start_kafka(topic_name)

    app.run(debug=True, port=5001)

