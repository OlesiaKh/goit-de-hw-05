from kafka import KafkaConsumer, KafkaProducer
import json

# Створюємо Consumer
consumer = KafkaConsumer(
    'building_sensors_olesia',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='sensor_processor_group'
)

# Створюємо Producer для алертів
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Consumer started. Listening to sensor data...")

for message in consumer:
    data = message.value
    sensor_id = data['sensor_id']
    temperature = data['temperature']
    humidity = data['humidity']

    if temperature > 40:
        alert = {
            "sensor_id": sensor_id,
            "temperature": temperature,
            "timestamp": data['timestamp'],
            "alert": "Temperature exceeded 40°C!"
        }
        print("⚠️ Temperature Alert:", alert)
        producer.send('temperature_alerts_olesia', value=alert)

    if humidity > 80 or humidity < 20:
        alert = {
            "sensor_id": sensor_id,
            "humidity": humidity,
            "timestamp": data['timestamp'],
            "alert": "Humidity out of range (20–80%)!"
        }
        print("⚠️ Humidity Alert:", alert)
        producer.send('humidity_alerts_olesia', value=alert)
