from pykafka import KafkaClient
import json
from datetime import datetime, timezone
import uuid
import time
import os


# get coordinates from file
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script's directory
file_path = os.path.join(script_dir, "data", "truck1.json") 
file = open(file_path)
coordinates = json.load(file)
coordinates = coordinates["features"][0]["geometry"]["coordinates"]

# Kafka producer
client = KafkaClient(hosts="localhost:9092")
topic = client.topics["geodata"]
producer = topic.get_sync_producer()

# for generating uuid
def generate_uuid():
    return uuid.uuid4()

# create message
data = {}
data["truck"] = "GRV-3254"
data["driver"] = "Torben Nightshade"

def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        # Extract latitude, longitude, and speed from the coordinates array
        longitude = coordinates[i][0]
        latitude = coordinates[i][1]
        speed = coordinates[i][2]

        # Update the data dictionary
        data["key"] = data["truck"] + "_" + str(generate_uuid())
        data["timestamp"] = str(datetime.now(timezone.utc))
        data["latitude"] = latitude
        data["longitude"] = longitude
        data["speed"] = speed  # Add speed to the data dictionary

        # Convert the data dictionary to a JSON string
        message = json.dumps(data)
        print(message)

        # Produce the message to Kafka (adjust topic as necessary)
        producer.produce(message.encode('ascii'))

        # seconds between sent coordinates
        time.sleep(1)
        i += 1


generate_checkpoint(coordinates)