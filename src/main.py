from confluent_kafka import Producer
from tqdm import tqdm
import argparse
import socket
import yaml
import os
import logging
import sys
from typing import List
from powergrader_event_utils.events import PowerGraderEvent, EventType
from powergrader_event_utils.testing import (
    create_demo_events,
    create_realistic_events_from_jsonl_test_output,
)
import time

JSONL_FILE_PATH = "./data/30_median_smart_benchmark/trial_reports.jsonl"


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
        time.sleep(0.1)


def duplicate_events(events: List[PowerGraderEvent], num_duplications: int = 10):
    duplicated_events = []
    for event in events:
        for _ in range(num_duplications):
            duplicated_events.append(event)

    return duplicated_events


def stratified_publish(events: List[PowerGraderEvent], producer: Producer, slow=False):
    # Sort events by event type
    events_by_type = {}
    for event in events:
        if event.event_type not in events_by_type:
            events_by_type[event.event_type] = []
        events_by_type[event.event_type].append(event)

    # Print options to the console
    while next_event_type := _print_available_event_options_and_get_next_event_type(
        events_by_type
    ):
        # Send the next event type
        for event in tqdm(events_by_type[next_event_type]):
            event.publish(producer)
            if slow:
                producer.flush()
                time.sleep(0.1)
        producer.flush()

        # Remove the event type from the list of available event types
        del events_by_type[next_event_type]

        if len(events_by_type.keys()) == 0:
            print("All events sent. Exiting.")
            break


def _print_available_event_options_and_get_next_event_type(events_by_type) -> EventType:
    print("Available event types to send:")
    sorted_event_types: List[EventType] = sorted(events_by_type.keys())
    for i, event_type in enumerate(sorted_event_types):
        print(f"{i+1}: {event_type.name}")
    print("Please enter the number corresponding to the event type you want to send.")

    # Get user input
    user_input = input()
    user_input = int(user_input)
    if user_input < 1 or user_input > len(sorted_event_types):
        print(
            "Invalid input. Please enter a number between 1 and",
            len(sorted_event_types),
        )

    print(f"Sending {sorted_event_types[user_input-1].name} events")
    return sorted_event_types[user_input - 1]


if __name__ == "__main__":
    logger = setup_logger("publish_test")

    # SETUP COMMAND ARGUMENTS
    parser = argparse.ArgumentParser(description="Example script with a boolean flag.")
    parser.add_argument("-s", action="store_true", help="Send events one at a time")
    parser.add_argument("-d", action="store_true", help="Send duplicate events")
    parser.add_argument(
        "--realistic", action="store_true", help="Send realistic events from JSONL file"
    )
    parser.add_argument(
        "--random", action="store_true", help="Send selected events in random order"
    )
    parser.add_argument(
        "--reverse", action="store_true", help="Send selected events in reverse order"
    )
    parser.add_argument(
        "--stratified",
        action="store_true",
        help="Send events by event type and only on user approval.",
    )
    args = parser.parse_args()

    SLOW = args.s
    DUPLICATE = args.d
    REALISTIC = args.realistic
    RANDOM = args.random
    STRATIFIED = args.stratified
    REVERSE = args.reverse

    MAIN_CFG_PATH = os.getenv("CLUSTER_CFG_FILE", "/srv/config.yaml")
    config_valid = True
    with open(MAIN_CFG_PATH, "r") as f:
        config = yaml.safe_load(f)
    if "KAFKA_PRODUCER" not in config:
        logger.error("KAFKA_PRODUCER not set in config")
        config_valid = False
    producer_config = config["KAFKA_PRODUCER"]

    producer = Producer(producer_config)
    print("Created producer")

    events_to_send = create_demo_events()

    if REALISTIC:
        print(f"Sending realistic events from {JSONL_FILE_PATH}")
        events_to_send = create_realistic_events_from_jsonl_test_output(JSONL_FILE_PATH)

    if DUPLICATE:
        print("Sending duplicate events")
        events_to_send = duplicate_events(events_to_send)

    if RANDOM:
        print("Sending events in random order")
        import random

        random.shuffle(events_to_send)
    elif REVERSE:
        print("Sending events in reverse order")
        events_to_send = events_to_send[::-1]

    if STRATIFIED:
        print("Sending events stratified by event type")
        stratified_publish(events_to_send, producer, slow=SLOW)

    if SLOW:
        print("Sending events one at a time")
        slow_publish(events_to_send, producer)
    else:
        print("Sending events in bulk")
        bulk_publish(events_to_send, producer)
