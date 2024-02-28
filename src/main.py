from confluent_kafka import Producer
from tqdm import tqdm
import argparse
import socket
import yaml
import os
import logging
import sys
from typing import List
from powergrader_event_utils.events import PowerGraderEvent
from powergrader_event_utils.testing import create_demo_events


def setup_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    format = logging.Formatter("{%(name)s: %(levelname)s, %(asctime)s, %(message)s}")

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(format)

    logger.addHandler(sh)

    return logger


def bulk_publish(events: List[PowerGraderEvent], producer: Producer):
    for event in tqdm(events):
        event.publish(producer)
    producer.flush()


def slow_publish(events: List[PowerGraderEvent], producer: Producer):
    for event in tqdm(events):
        event.publish(producer)
        producer.flush()


def duplicate_publish(events: List[PowerGraderEvent], producer: Producer):
    event_to_duplicate = events[4]

    print(f"Publishing {event_to_duplicate.event_type} event multiple times")
    for _ in tqdm(range(1000)):
        event_to_duplicate.publish(producer)
    producer.flush()


if __name__ == "__main__":
    logger = setup_logger("publish_test")

    # SETUP COMMAND ARGUMENTS
    parser = argparse.ArgumentParser(description="Example script with a boolean flag.")
    parser.add_argument("-s", action="store_true", help="Send events one at a time")
    parser.add_argument("-d", action="store_true", help="Send duplicate events")
    args = parser.parse_args()

    SLOW = args.s
    DUPLICATE = args.d

    MAIN_CFG_PATH = os.getenv("CLUSTER_CFG_FILE", "/srv/config.yaml")
    config_valid = True
    with open(MAIN_CFG_PATH, "r") as f:
        config = yaml.safe_load(f)
    if "KAFKA_PRODUCER" not in config:
        logger.error("KAFKA_PRODUCER not set in config")
        config_valid = False
    producer_config = config["KAFKA_PRODUCER"]

    conf = {
        "bootstrap.servers": "power_kafka:9092",
        # 'security.protocol': 'SASL_SSL',
        # 'sasl.mechanism': 'PLAIN',
        # 'sasl.username': '<CLUSTER_API_KEY>',
        # 'sasl.password': '<CLUSTER_API_SECRET>',
        "linger.ms": 30,
        "client.id": socket.gethostname(),
    }

    producer = Producer(producer_config)
    print("Created producer")

    events_to_send = create_demo_events()

    if SLOW:
        slow_publish(events_to_send, producer)
    elif DUPLICATE:
        duplicate_publish(events_to_send, producer)
    else:
        bulk_publish(events_to_send, producer)
