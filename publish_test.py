from powergrader_event_utils.events.assignment import AssignmentEvent, RubricEvent
from powergrader_event_utils.events import (
    RegisterCoursePublicIDEvent,
    InstructorEvent,
    RubricCriterion,
    CriteriaLevel,
    OrganizationEvent,
    CriteriaGradeEvent,
    CriteriaGradeEmbeddingEvent,
    GradingStartedEvent,
    InstructorReviewEvent,
    SubmissionFilesEvent,
    SubmissionEvent,
    StudentEvent,
    FileContent,
)
from powergrader_event_utils.events.base import MAIN_TOPIC
from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer
from uuid import uuid4
from random import randint

print("Starting the script")
org_event = OrganizationEvent(name="test", code=None)

print("Creating instructor")
instructor = InstructorEvent(
    org_id=org_event.id, name="Mr.Bean", email="bean@email.com"
)


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
# Package the criteria into a RubricCriterion object
criterion = {}
for key, value in criteria.items():
    criterion[key] = RubricCriterion(
        name=value["name"],
        id=str(uuid4()),
        levels=[
            CriteriaLevel(description=level["description"], score=level["score"])
            if "score" in level
            else CriteriaLevel(description=level["description"], score=None)
            for level in value["levels"]
        ],
    )
rub_event = RubricEvent(
    instructor_id=instructor.id, name="Test Rubric #1", rubric_criteria=criterion
)
rub_criteria = rub_event.rubric_criteria
for crit in rub_criteria.values():
    print(crit.name)
    for level in crit.levels:
        print("\t", level.description)
        print("\t", level.score)
# print(rub_event.serialize())
print(type(rub_event.serialize()))
serialized = rub_event.serialize()

new_rub_event = RubricEvent.deserialize(serialized)
new_rub_criteria = new_rub_event.rubric_criteria
print("\n\nNEW DESERIALIZED EVENT\n\n")
for crit in new_rub_criteria.values():
    print(crit.name)
    for level in crit.levels:
        print("\t", level.description)
        print("\t", level.score)

print("Creating assignment event")
instructions = """Assignment 4: Recursion

Write a Python program to get the Fibonacci number at N.

Note : The Fibonacci Sequence is the series of numbers :
0, 1, 1, 2, 3, 5, 8, 13, 21, ....
Every next number is found by adding up the two numbers before it.

Remember to implement your solution using recursion. 
The final program should take user input from the terminal specifying the desired Fibonacci number and display the calculated result. 
(Note: The first entry is N=1)"""
ass_event = AssignmentEvent(
    rubric_id=rub_event.id, name="Fibonacci", instructions=instructions
)
# print(ass_event.validate())
print(ass_event.serialize())
print(type(ass_event.serialize()))

print("Creating RegisterCoursePublicIdEvent")
# reg_course = RegisterCoursePublicIDEvent(
#     public_id=str(uuid4()), lms_id=str(randint(0, 100000000))
# )
reg_course = RegisterCoursePublicIDEvent(public_id=str(uuid4()), lms_id="1")
print(reg_course.serialize())

print("Creating Student event")
student = StudentEvent(
    org_id=org_event.id, name="Jimmy Newtron", email="jimmy@email.com"
)

print("Creating Submission Files Event")
file_content = """def fibonacci(n):
    \"\"\"
    Calculates the Fibonacci number at the given position and generates the Fibonacci series up to that position using recursion.

    Args:
        n (int): The position of the Fibonacci number.

    Returns:
        list: The Fibonacci series up to the given position.
    \"\"\"
    if n <= 0:
        raise ValueError("Invalid input. Please enter a positive integer.")
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        series = fibonacci(n - 1)
        series.append(series[-1] + series[-2])
        return series


def main():
    \"\"\"
    Entrypoint of the program.
    \"\"\"
    try:
        n = int(input("Enter the position of the Fibonacci number: "))
        series = fibonacci(n)

        print(f"The Fibonacci series up to position {n} is:")
        for i, num in enumerate(series, start=1):
            print(f"{i}: {num}")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")


if __name__ == "__main__":
    main()"""
file_obj = FileContent(file_name="submission", file_type="py", content=file_content)
sub_files = SubmissionFilesEvent(student_id=student.id, file_content=[file_obj])

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

print("Sending org event")
org_event.publish(producer)

print("Sending INstructor event")
instructor.publish(producer)


print("Sending Rubric event")
rub_event.publish(producer)

print("Sending Assignment event")
ass_event.publish(producer)

# reg_course.publish(producer)
# reg_course.publish(producer)
print("Published the reg_course event")

producer.commit_transaction()
