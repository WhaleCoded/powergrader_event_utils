from confluent_kafka import Producer
from tqdm import tqdm
from integration.demo_events import create_demo_events
import argparse
import socket
import yaml
import os
import logging
import sys
from typing import List
from powergrader_event_utils.events import PowerGraderEvent


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


if __name__ == "__main__":
    logger = setup_logger("publish_test")

    # SETUP COMMAND ARGUMENTS
    parser = argparse.ArgumentParser(description="Example script with a boolean flag.")
    parser.add_argument("-s", action="store_true", help="Send events one at a time")
    args = parser.parse_args()

    SLOW = args.s

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
        for event in tqdm(events_to_send):
            event.publish(producer)
            producer.flush()
    else:
        for event in tqdm(events_to_send):
            event.publish(producer)
        producer.flush()
