from confluent_kafka import Consumer
from powergrader_event_utils.events.base import MAIN_TOPIC
from powergrader_event_utils.events import deserialize_powergrader_event
import sys
from confluent_kafka import KafkaError, KafkaException

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "test",
    "auto.offset.reset": "smallest",
}

consumer = Consumer(conf)
print("Created kafka consumer")


running = True


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(msg.headers())
                headers = msg.headers()
                event_type_header = [h[1] for h in headers if h[0] == "event_type"]

                if len(event_type_header) > 0:
                    serialized_event = msg.value()
                    print(serialized_event)
                    event_type = event_type_header[0]
                    event = deserialize_powergrader_event(event_type, serialized_event)
                    print(event)
                    if event_type == b"AssignmentEvent":
                        print(event.get_rubric_id())
                        print(event.get_name())
                        print(event.get_instructions())
                    elif event_type == b"RubricEvent":
                        print(event.get_instructor_id())
                        print(event.get_criteria())
                        print(event.get_id())
                else:
                    print("No event type header found")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    running = False


basic_consume_loop(consumer, [MAIN_TOPIC])
