from powergrader_event_utils.events.assignment import AssignmentEvent, RubricEvent
from powergrader_event_utils.events import (
    CourseEvent,
    SectionEvent,
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
    GradeType,
    GradeIdentifier,
    AssignmentAddedToCourseEvent,
    AssignmentRemovedFromCourseEvent,
    StudentAddedToSectionEvent,
    StudentRemovedFromSectionEvent,
    InstructorAddedToCourseEvent,
    InstructorRemovedFromCourseEvent,
    convert_proto_when_to_date_time,
    RetryEvent,
    LMSInstructorType,
    RegisterInstructorPublicIDEvent,
    RegisterStudentPublicIDEvent,
    RegisterSectionPublicIDEvent,
    RegisterAssignmentPublicIDEvent,
    RegisterRubricPublicIDEvent,
    RegisterSubmissionPublicIDEvent,
    PublishedToLMSEvent,
    PublishedGradeToLMSEvent,
)
from powergrader_event_utils.events.base import MAIN_TOPIC
from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer
from uuid import uuid4
from random import randint
import datetime
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

events_to_send = []


def get_miliseconds_since_epoch():
    return int(time.time_ns() / 1_000_000)


print("Starting the script")
when = int(time.time())
org_event = OrganizationEvent(name="Dallin University", code=str(uuid4()))
events_to_send.append(org_event)

print("Creating instructor")
instructor = InstructorEvent(
    organization_id=org_event.id,
    name="Mr.Bean",
    email="bean@email.com",
    when=get_miliseconds_since_epoch(),
)
events_to_send.append(instructor)

course = CourseEvent(
    organization_id=org_event.id,
    instructor_id=instructor.public_id,
    name="CS 101",
    description=None,
    when=get_miliseconds_since_epoch(),
)
events_to_send.append(course)


section = SectionEvent(
    course_id=course.public_id,
    name="Section 1",
    when=get_miliseconds_since_epoch(),
    is_active=True,
)
events_to_send.append(section)


print("Creating Student event")
student = StudentEvent(
    organization_id=org_event.id,
    name="Jimmy Newtron",
    email="jimmy@email.com",
    when=get_miliseconds_since_epoch(),
)
events_to_send.append(student)

time.sleep(0.1)
# for i in range(10):
#     update_course = CourseEvent(
#         organization_id=org_event.id,
#         instructor_id=instructor.public_id,
#         name="CS 42",
#         description=None,
#         when=get_miliseconds_since_epoch(),
#         public_id=course.public_id,
#     )
#     events_to_send.append(update_course)
time.sleep(0.1)
update_course = CourseEvent(
    organization_id=org_event.id,
    instructor_id=instructor.public_id,
    name="FINAL EVENT MADE IT CORRECTLY",
    description=None,
    when=get_miliseconds_since_epoch(),
    public_id=course.public_id,
)
events_to_send.append(update_course)

update_section = SectionEvent(
    course_id=course.public_id,
    name="Section 42",
    when=get_miliseconds_since_epoch(),
    is_active=False,
    public_id=section.public_id,
)
print(update_section.is_active)
unserialized_section = SectionEvent.deserialize(update_section.serialize())
print(unserialized_section.is_active)
events_to_send.append(update_section)

update_instructor = InstructorEvent(
    organization_id=org_event.id,
    name="Senor Bean",
    email="bean@email.com",
    when=get_miliseconds_since_epoch(),
    public_id=instructor.public_id,
)
events_to_send.append(update_instructor)

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
    instructor_id=instructor.public_id, name="Test Rubric #1", rubric_criteria=criterion
)
events_to_send.append(rub_event)

new_crit = {"New Crit": RubricCriterion(name="New Crit", id=str(uuid4()), levels=[])}
power_grader_rubric = RubricEvent(
    instructor_id=None, name="PowerGrader Default #1", rubric_criteria=new_crit
)
events_to_send.append(power_grader_rubric)

rub_criteria = rub_event.rubric_criteria
# for crit in rub_criteria.values():
#     print(crit.name)
#     for level in crit.levels:
#         print("\t", level.description)
#         print("\t", level.score)
# print(rub_event.serialize())

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
    rubric_id=rub_event.id,
    name="Fibonacci",
    instructions=instructions,
    organization_id=org_event.id,
)
events_to_send.append(ass_event)

incomplete_assingment = AssignmentEvent(
    rubric_id=None,
    organization_id=org_event.id,
    name="Incomplete Test",
    instructions=None,
)
events_to_send.append(incomplete_assingment)

# print("Creating RegisterCoursePublicIdEvent")
# # reg_course = RegisterCoursePublicIDEvent(
# #     public_id=str(uuid4()), lms_id=str(randint(0, 100000000))
# # )
# reg_course = RegisterCoursePublicIDEvent(public_id=str(uuid4()), lms_id="1")
# print(reg_course.serialize())
# events_to_send.append(reg_course)


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
sub_files = SubmissionFilesEvent(student_id=student.public_id, file_content=[file_obj])
events_to_send.append(sub_files)

# print("Creating Submission Event")
sub_event = SubmissionEvent(
    student_id=student.public_id,
    assignment_id=ass_event.id,
    submission_files_id=sub_files.id,
    when=get_miliseconds_since_epoch(),
)
events_to_send.append(sub_event)


print("Create AI Grading Started Event")
crit_ids = [crit.id for crit in rub_event.rubric_criteria.values()]
ai_grade_event = GradingStartedEvent(sub_event.id, "GPT-3.5 Turbo", crit_ids)
events_to_send.append(ai_grade_event)

# print("Create ai graded crit event")
crit_graded = CriteriaGradeEvent(
    ai_grade_event.id, crit_ids[0], GradeType.AI_GRADED, 1, "Their code did not run."
)
events_to_send.append(crit_graded)

# print("Create Faculty graded crit event")
grade_identifier = GradeIdentifier(sub_event.id, instructor.public_id, None)
faculty_crit_graded = CriteriaGradeEvent(
    grade_identifier,
    crit_ids[1],
    GradeType.FACULTY_ADJUSTED,
    3,
    "The student's code was nearly flawless",
)
events_to_send.append(faculty_crit_graded)

print("Create criteria grade embeddigns")
ai_grade_embedding = CriteriaGradeEmbeddingEvent(
    crit_graded.id, "Roberta-3", [0.0 for i in range(20)]
)
events_to_send.append(ai_grade_embedding)
faculty_grade_embedding = CriteriaGradeEmbeddingEvent(
    faculty_crit_graded.id, "Roberta-3", [1.0 for i in range(20)]
)
events_to_send.append(faculty_grade_embedding)

# print("Create instructor review event")
instructor_review_event = InstructorReviewEvent(
    sub_event.id,
    instructor.public_id,
    time_reviewed=get_miliseconds_since_epoch(),
    criteria_grade_ids=[crit_graded.id, faculty_crit_graded.id],
)
events_to_send.append(instructor_review_event)

# # PUBLISH EVENTS
lms_course = RegisterCoursePublicIDEvent(
    public_id=course.public_id, lms_id=str(randint(0, 100000000))
)
events_to_send.append(lms_course)

lms_section = RegisterSectionPublicIDEvent(
    public_id=section.public_id, lms_id=str(randint(0, 100000000))
)
events_to_send.append(lms_section)

lms_student = RegisterStudentPublicIDEvent(
    public_id=student.public_id, lms_id=str(randint(0, 100000000))
)
events_to_send.append(lms_student)

lms_instructor = RegisterInstructorPublicIDEvent(
    public_id=instructor.public_id,
    lms_id=str(randint(0, 100000000)),
    user_type=LMSInstructorType.FACULTY,
)
events_to_send.append(lms_instructor)

lms_assignment = RegisterAssignmentPublicIDEvent(
    public_id=str(uuid4()),
    lms_id=str(randint(0, 100000000)),
    organization_id=org_event.id,
)
events_to_send.append(lms_assignment)

lms_rubric = RegisterRubricPublicIDEvent(
    public_id=str(uuid4()),
    lms_id=str(randint(0, 100000000)),
    organization_id=org_event.id,
)
events_to_send.append(lms_rubric)

lms_submission = RegisterSubmissionPublicIDEvent(
    public_id=str(uuid4()),
    lms_assignment_id=lms_assignment.lms_id,
    lms_student_id=lms_student.lms_id,
    organization_id=org_event.id,
)
events_to_send.append(lms_submission)

# Test the actual publish event
when = get_miliseconds_since_epoch()
publish_course = PublishedToLMSEvent(
    public_id_of_published_entity=lms_course.public_id,
    private_id_of_published_entity=course.id,
    when=when,
)
events_to_send.append(publish_course)

publish_section = PublishedToLMSEvent(
    public_id_of_published_entity=lms_section.public_id,
    private_id_of_published_entity=section.id,
    when=when,
)
events_to_send.append(publish_section)

publish_student = PublishedToLMSEvent(
    public_id_of_published_entity=lms_student.public_id,
    private_id_of_published_entity=student.id,
    when=when,
)
events_to_send.append(publish_student)

publish_instructor = PublishedToLMSEvent(
    public_id_of_published_entity=lms_instructor.public_id,
    private_id_of_published_entity=instructor.id,
    when=when,
)
events_to_send.append(publish_instructor)

publish_assignment = PublishedToLMSEvent(
    public_id_of_published_entity=lms_assignment.public_id,
    private_id_of_published_entity=ass_event.id,
    when=when,
)
events_to_send.append(publish_assignment)

publish_rubric = PublishedToLMSEvent(
    public_id_of_published_entity=lms_rubric.lms_id,
    private_id_of_published_entity=rub_event.id,
    when=when,
)
events_to_send.append(publish_rubric)

publish_submission = PublishedToLMSEvent(
    public_id_of_published_entity=lms_submission.public_id,
    private_id_of_published_entity=sub_event.id,
    when=when,
)
events_to_send.append(publish_assignment)

publish_grade = PublishedGradeToLMSEvent(
    public_submission_id=lms_submission.public_id,
    instructor_review_id=instructor_review_event.id,
    when=when,
)
events_to_send.append(publish_grade)
# # RELATIONSHIP
# add_assignment_to_course = AssignmentAddedToCourseEvent(ass_event.id, course.id)
# events_to_send.append(add_assignment_to_course)

# remove_assignment_to_course = AssignmentRemovedFromCourseEvent(ass_event.id, course.id)
# events_to_send.append(remove_assignment_to_course)

# second_add_to_course = AssignmentAddedToCourseEvent(ass_event.id, course.id)
# events_to_send.append(second_add_to_course)

# instructor_added_to_course = InstructorAddedToCourseEvent(instructor.id, course.id)
# events_to_send.append(instructor_added_to_course)

# instructor_removed_from_course = InstructorRemovedFromCourseEvent(
#     instructor.id, course.id
# )
# events_to_send.append(instructor_added_to_course)

# send_instructor_add = InstructorAddedToCourseEvent(instructor.id, course.id)
# events_to_send.append(send_instructor_add)

# student_added_section = StudentAddedToSectionEvent(student.id, section.id)
# events_to_send.append(student_added_section)

# student_removed_section = StudentRemovedFromSectionEvent(student.id, section.id)
# events_to_send.append(student_removed_section)

# student_added_section = StudentAddedToSectionEvent(student.id, section.id)
# events_to_send.append(student_added_section)

import socket

conf = {
    "bootstrap.servers": "localhost:9092",
    # 'security.protocol': 'SASL_SSL',
    # 'sasl.mechanism': 'PLAIN',
    # 'sasl.username': '<CLUSTER_API_KEY>',
    # 'sasl.password': '<CLUSTER_API_SECRET>',
    "linger.ms": 30,
    "client.id": socket.gethostname(),
}

producer = Producer(conf)
print("Created producer")

for event in tqdm(events_to_send):
    event.publish(producer)
    # producer.flush()
    # producer.commit_transaction()
producer.flush()


# def publish_event(event):
#     producer = Producer(conf)
#     # print("Created producer")
#     producer.init_transactions()

#     producer.begin_transaction()
#     event.publish(producer)
#     producer.flush()
#     producer.commit_transaction()


# # Publish all the events simultaneously
# with ThreadPoolExecutor() as executor:
#     futures = []
#     for event in events_to_send:
#         futures.append(executor.submit(publish_event, event))

#     for future in tqdm(futures):
#         future.result()


# producer.commit_transaction()
