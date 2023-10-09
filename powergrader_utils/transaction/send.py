from kafka import KafkaProducer

MAIN_TOPIC = "main-record"


def publish_event(event, server: str):
    if event is None:
        return

    producer = KafkaProducer(bootstrap_servers=server)
    producer.send(MAIN_TOPIC, event.encode("utf-8"))
    producer.flush()
    producer.close()
