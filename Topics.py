from kafka.admin import KafkaAdminClient

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id='check_topics'
)

for topic in admin_client.list_topics():
    if 'olesia' in topic:  #
        print(topic)
