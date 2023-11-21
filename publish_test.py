from powergrader_event_utils.events.assignment import AssignmentEvent, RubricEvent
from powergrader_event_utils.events.base import MAIN_TOPIC
from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer

print("Starting the script")


criteria = {
    "Functionality": {
        "name": "Functionality",
        "levels": [
            {
                "description": "The program does not run due to syntax errors. Behavior is entirely incorrect or incomplete.",
                "score": 0,
            },
            {
                "description": "The program runs, but will throw uncaught errors. Behavior is significantly incorrect or incomplete.",
                "score": 1,
            },
            {
                "description": "The program runs, but will throw uncaught errors for valid user input. The program may contain significant behavior errors.",
                "score": 2,
            },
            {
                "description": "The program runs and will only error out when given invalid user input. The program may have some unexpected behavior.",
                "score": 3,
            },
            {
                "description": "The program does not error out for any user input. The program produces valid outputs for all valid inputs. Behavior is correct and complete.",
                "score": 4,
            },
        ],
    },
    "Requirements": {
        "name": "Requirements",
        "levels": [
            {
                "description": "Program does not implement the fibonacci sequence. No recursion is present.",
                "score": 0,
            },
            {
                "description": "Program is missing either the fibonacci sequence or recursion.",
                "score": 1,
            },
            {
                "description": "Program implements the fibonacci sequence recursively, but does not start at N=1.",
                "score": 2,
            },
            {
                "description": "Program implements the fibonacci sequence recursively, correctly starting at N=1.",
                "score": 3,
            },
        ],
    },
    "Organization": {
        "name": "Organization",
        "levels": [
            {
                "description": "Program contains no attempt at organization. Significant use of global state. Behavior may not be contained in functions.",
                "score": 0,
            },
            {
                "description": "Program has very poor organization. Some use of global state. Most behavior is contained in functions.",
                "score": 1,
            },
            {
                "description": "Program displays decent organization. There is minimal use of global state, and all behavior is contained in functions.",
                "score": 2,
            },
            {
                "description": "Program is organized well. There is no use of global state, and all behavior is contained in functions. Entrypoint is clearly defined and dunder main is used.",
                "score": 3,
            },
        ],
    },
    "Documentation": {
        "name": "Documentation",
        "levels": [
            {
                "description": "Program contains no documentation. No docstrings or comments are present.",
                "score": 0,
            },
            {
                "description": "Program contains minimal documentation. Some docstrings or comments are present.",
                "score": 1,
            },
            {
                "description": "Program contains decent documentation. All functions have docstrings and comments are present where necessary.",
                "score": 2,
            },
            {
                "description": "Program contains good documentation. All functions have docstrings and comments are present where necessary. Docstrings are descriptive, and comments disambiguate code.",
                "score": 3,
            },
        ],
    },
}
print("Creating rubric event")
# # rub_event = RubricEvent(instructor_id="Mr.Bean", criteria=criteria)
# print(rub_event.validate())
# print(rub_event.serialize())
# print(type(rub_event.serialize()))

print("Creating assignment event")
ass_event = AssignmentEvent(rubric_id=None, name="good soup", instructions="kylo ren")
# print(ass_event.validate())
print(ass_event.serialize())
print(type(ass_event.serialize()))

import socket

conf = {
    "bootstrap.servers": "localhost:9092",
    # 'security.protocol': 'SASL_SSL',
    # 'sasl.mechanism': 'PLAIN',
    # 'sasl.username': '<CLUSTER_API_KEY>',
    # 'sasl.password': '<CLUSTER_API_SECRET>',
    "transactional.id": "test",
    "client.id": socket.gethostname(),
}

producer = Producer(conf)
print("Created producer")
producer.init_transactions()
producer.begin_transaction()


print("Sending Rubric event")
# rub_event.publish(producer)

print("Sending Assignment event")
ass_event.publish(producer)

producer.commit_transaction()
