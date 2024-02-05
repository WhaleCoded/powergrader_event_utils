from powergrader_event_utils.events.assignment import AssignmentEvent, RubricEvent
from powergrader_event_utils.events import (
    AssignmentEvent,
    CriterionLevel,
    RubricCriterion,
    RubricEvent,
    CourseEvent,
    SectionEvent,
    OrganizationEvent,
    AICriterionGradingStartedEvent,
    GradingMethodEvent,
    Grade,
    AICriterionGradeEvent,
    AIInferredCriterionGradeEvent,
    InstructorCriterionGradeEvent,
    InstructorOverrideCriterionGradeEvent,
    CriterionGradeEmbeddingEvent,
    InstructorSubmissionGradeApprovalEvent,
    RegisterCoursePublicUUIDEvent,
    RegisterSectionPublicUUIDEvent,
    RegisterInstructorPublicUUIDEvent,
    RegisterStudentPublicUUIDEvent,
    RegisterAssignmentPublicUUIDEvent,
    RegisterRubricPublicUUIDEvent,
    RegisterSubmissionPublicUUIDEvent,
    PublishedToLMSEvent,
    PublishedGradeToLMSEvent,
    AssignmentAddedToCourseEvent,
    AssignmentRemovedFromCourseEvent,
    StudentAddedToSectionEvent,
    StudentRemovedFromSectionEvent,
    InstructorAddedToCourseEvent,
    InstructorRemovedFromCourseEvent,
    FileContent,
    SubmissionFileGroupEvent,
    SubmissionEvent,
    StudentEvent,
    InstructorEvent,
)
from time import sleep
from powergrader_event_utils.events.base import MAIN_TOPIC
from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer
from uuid import uuid4
from random import randint
import datetime
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

bad_values = [
    "None",
    "False",
    "0",
    "-1",
    "Some super long really terrible no good very bad name that is just too long to be a name, but is just for testing purposes. I hope this is long enough to break something hahahahah. Evil laugh.",
    "123045",
    "\n",
    " ",
    "",
]

organization_names = [
    "Dallin University",
    "Apporto Test",
    "BYU",
    "UVU",
    "BYUI",
    "USU",
] + bad_values

instructor_names = [
    "Mr.Bean",
    "Senor Bean",
    "Dr.Bean",
    "Professor Bean",
    "Ms. Bean",
    "Dallin",
    "Antony",
    "Tanner",
    "Mr. H",
] + bad_values

emails = [
    "email@example.com",
    "firstname.lastname@example.com",
    "email@subdomain.example.com",
    "firstname+lastname@example.com",
    "email@123.123.123.123",
    "email@[123.123.123.123]",
    '"email"@example.com',
    "1234567890@example.com",
    "email@example-one.com",
    "_______@example.com",
    "email@example.name",
    "email@example.museum",
    "email@example.co.jp",
    "firstname-lastname@example.com",
] + bad_values

course_names = [
    "CS 101",
    "Macro Biology",
    "Intro to Python",
    "History of Central East Asia",
    "Intro to Calculus",
    "BIO 3050",
    "CS 102",
] + bad_values

descriptions = [
    "This is a description",
    "This is an even longer description",
    "And this is a description which defies all expectations of length. In fact, it is so long that it is hard to believe that it is a description at all. It is more like a novel. A novel about a description. A description novel. A descriptovel.",
    "There once was a description from Nantucket, whose length was so long it could not be",
    "This course is about the history of the world. It is a very long course, and it is very difficult. You will learn a lot, but you will also have to work very hard. It is not for the faint of heart.",
] + bad_values

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

rubric_names = [
    "Fibonacci",
    "Recursion",
    "Python",
    "CS 101",
    "BIO 3050",
    "Intro to Python",
] + bad_values


def get_miliseconds_since_epoch():
    return int(time.time_ns() / 1_000_000)


def create_org_worth_of_events():
    events_to_send = []

    print("Starting the script")
    when = int(time.time())
    org_event = OrganizationEvent(
        public_uuid=str(uuid4()), name="Dallin University", version_timestamp=when
    )
    events_to_send.append(org_event)

    apporto_test_event = OrganizationEvent(
        public_uuid=str(uuid4()), name="Apporto Test", version_timestamp=when
    )
    events_to_send.append(apporto_test_event)

    print("Creating instructor")
    register_instructor = RegisterInstructorPublicUUIDEvent(
        lms_id=str(randint(0, 100000000)),
        user_type=2,
        organization_public_uuid=org_event.public_uuid,
    )
    events_to_send.append(register_instructor)
    instructor = InstructorEvent(
        public_uuid=register_instructor.public_uuid,
        name="Mr.Bean",
        email="bean@email.com",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(instructor)

    time.sleep(0.1)

    instructor = InstructorEvent(
        public_uuid=register_instructor.public_uuid,
        name="Mr.Bean",
        email="bean02@email.com",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(instructor)

    register_course = RegisterCoursePublicUUIDEvent(
        lms_id=str(randint(0, 100000000)),
        organization_public_uuid=org_event.public_uuid,
    )
    events_to_send.append(register_course)
    course = CourseEvent(
        public_uuid=register_course.public_uuid,
        instructor_public_uuid=instructor.public_uuid,
        name=course_names[randint(0, len(course_names) - 1)],
        description=descriptions[randint(0, len(descriptions) - 1)],
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(course)

    register_section = RegisterSectionPublicUUIDEvent(
        lms_id=str(randint(0, 100000000)),
        organization_public_uuid=org_event.public_uuid,
    )
    events_to_send.append(register_section)
    section = SectionEvent(
        public_uuid=register_section.public_uuid,
        course_public_uuid=course.public_uuid,
        name="Section 1",
        closed=False,
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(section)

    print("Creating Student event")
    register_student = RegisterStudentPublicUUIDEvent(
        lms_id=str(randint(0, 100000000)),
        organization_public_uuid=org_event.public_uuid,
    )
    events_to_send.append(register_student)
    student = StudentEvent(
        public_uuid=register_student.public_uuid,
        name="Dallin",
        email="d@apporto.com",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(student)

    time.sleep(0.1)
    time.sleep(0.1)
    update_course = CourseEvent(
        public_uuid=course.public_uuid,
        instructor_public_uuid=instructor.public_uuid,
        name="FINAL EVENT MADE IT CORRECTLY",
        description=descriptions[randint(0, len(descriptions) - 1)],
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(update_course)
    time.sleep(0.1)
    time.sleep(0.1)
    update_section = SectionEvent(
        public_uuid=section.public_uuid,
        course_public_uuid=course.public_uuid,
        name="Section 42",
        closed=True,
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(update_section)

    print("Creating rubric event")
    # Package the criteria into a RubricCriterion object
    criterion = {}
    for key, value in criteria.items():
        criterion[key] = RubricCriterion(
            name=value["name"],
            id=str(uuid4()),
            levels=[
                (
                    CriterionLevel(
                        description=level["description"], score=level["score"]
                    )
                    if "score" in level
                    else CriterionLevel(description=level["description"], score=None)
                )
                for level in value["levels"]
            ],
        )
    register_rubric = RegisterRubricPublicUUIDEvent(
        lms_id=str(randint(0, 100000000)),
        organization_public_uuid=org_event.public_uuid,
    )
    rub_event = RubricEvent(
        public_uuid=register_rubric.public_uuid,
        instructor_public_uuid=instructor.public_uuid,
        name=rubric_names[randint(0, len(rubric_names) - 1)],
        rubric_criteria=criterion,
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(rub_event)

    new_crit = {
        "New Crit": RubricCriterion(name="New Crit", id=str(uuid4()), levels=[])
    }
    power_grader_rubric = RubricEvent(
        public_uuid=register_rubric.public_uuid,
        instructor_public_uuid=instructor.public_uuid,
        name="PowerGrader Rubric",
        rubric_criteria=new_crit,
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(power_grader_rubric)

    print("Creating assignment event")
    instructions = """Assignment 4: Recursion

    Write a Python program to get the Fibonacci number at N.

    Note : The Fibonacci Sequence is the series of numbers :
    0, 1, 1, 2, 3, 5, 8, 13, 21, ....
    Every next number is found by adding up the two numbers before it.

    Remember to implement your solution using recursion.
    The final program should take user input from the terminal specifying the desired Fibonacci number and display the calculated result.
    (Note: The first entry is N=1)"""
    register_assignment = RegisterAssignmentPublicUUIDEvent(
        lms_id=str(randint(0, 100000000)),
        organization_public_uuid=org_event.public_uuid,
    )
    ass_event = AssignmentEvent(
        public_uuid=register_assignment.public_uuid,
        rubric_version_uuid=rub_event.version_uuid,
        name="Recursion",
        description="An assignment",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events_to_send.append(ass_event)

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
    sub_files = SubmissionFileGroupEvent(
        student_public_uuid=register_student.public_uuid, files=[file_obj]
    )
    events_to_send.append(sub_files)

    # print("Creating Submission Event")
    sub_event = SubmissionEvent(
        public_uuid=str(uuid4()),
        student_public_uuid=student.public_uuid,
        assignment_version_uuid=ass_event.version_uuid,
        submission_file_group_uuid=sub_files.uuid,
        version_timestamp=get_miliseconds_since_epoch(),
    )

    events_to_send.append(sub_event)

    print("Create AI Grading Started Event")
    crit_ids = [crit.id for crit in rub_event.rubric_criteria.values()]
    ai_grade_event = GradingStartedEvent(sub_event.id, "GPT-3.5 Turbo", crit_ids)
    events_to_send.append(ai_grade_event)

    # print("Create ai graded crit event")
    crit_graded = CriteriaGradeEvent(
        ai_grade_event.id,
        crit_ids[0],
        GradeType.AI_GRADED,
        1,
        "Their code did not run.",
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
        public_id_of_published_entity=lms_rubric.public_id,
        private_id_of_published_entity=rub_event.id,
        when=when,
    )
    events_to_send.append(publish_rubric)

    publish_submission = PublishedToLMSEvent(
        public_id_of_published_entity=lms_submission.public_id,
        private_id_of_published_entity=sub_event.id,
        when=when,
    )
    events_to_send.append(publish_submission)

    publish_grade = PublishedGradeToLMSEvent(
        public_submission_id=lms_submission.public_id,
        instructor_review_id=instructor_review_event.id,
        when=when,
    )
    events_to_send.append(publish_grade)
    # # RELATIONSHIP
    add_assignment_to_course = AssignmentAddedToCourseEvent(
        ass_event.id, course.public_id
    )
    events_to_send.append(add_assignment_to_course)

    remove_assignment_to_course = AssignmentRemovedFromCourseEvent(
        ass_event.id, course.public_id
    )
    events_to_send.append(remove_assignment_to_course)

    second_add_to_course = AssignmentAddedToCourseEvent(ass_event.id, course.public_id)
    events_to_send.append(second_add_to_course)

    instructor_added_to_course = InstructorAddedToCourseEvent(
        instructor.public_id, course.public_id
    )
    events_to_send.append(instructor_added_to_course)

    instructor_removed_from_course = InstructorRemovedFromCourseEvent(
        instructor.public_id, course.public_id
    )
    events_to_send.append(instructor_removed_from_course)

    send_instructor_add = InstructorAddedToCourseEvent(
        instructor.public_id, course.public_id
    )
    events_to_send.append(send_instructor_add)

    student_added_section = StudentAddedToSectionEvent(
        student.public_id, section.public_id
    )
    events_to_send.append(student_added_section)

    student_removed_section = StudentRemovedFromSectionEvent(
        student.public_id, section.public_id
    )
    events_to_send.append(student_removed_section)

    student_added_section = StudentAddedToSectionEvent(
        student.public_id, section.public_id
    )
    events_to_send.append(student_added_section)

    return events_to_send


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

events_to_send = []
for i in range(1):
    events_to_send.extend(create_org_worth_of_events())

for event in tqdm(events_to_send):
    event.publish(producer)
    producer.flush()
    sleep(1)
    # producer.commit_transaction()
# producer.flush()


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

# ----------------------------------------------------------------

# def create_assignment(organization_id, instructor_id, timestamp) -> (list, str):
#     register = RegisterRubricPublicUUIDEvent(
#         lms_id=str(randint(0, 100000000)), organization_public_uuid=organization_id
#     )
#     timestamp = timestamp + randint(0, 100000)
#     rubric = RubricEvent(
#         public_uuid=register.public_uuid,
#         instructor_public_uuid=instructor_id,
#         name=rubric_names[randint(0, len(rubric_names) - 1)],
#         rubric_criteria={
#             key: RubricCriterion(
#                 uuid=str(uuid4()),
#                 name=value["name"],
#                 levels=[
#                     CriterionLevel(
#                         score=level["score"], description=level["description"]
#                     )
#                     for level in value["levels"]
#                 ],
#             )
#             for key, value in criteria.items()
#         },
#         version_timestamp=timestamp,
#     )
#     register = RegisterAssignmentPublicUUIDEvent(
#         lms_id=str(randint(0, 100000000)), organization_public_uuid=organization_id
#     )
#     timestamp = timestamp + randint(0, 100000)
#     assignment = AssignmentEvent(
#         public_uuid=register.public_uuid,
#         rubric_version_uuid=rubric.version_uuid,
#         name=rubric_names[randint(0, len(rubric_names) - 1)],
#         description=descriptions[randint(0, len(descriptions) - 1)],
#         version_timestamp=timestamp,
#     )
#     events = [register, rubric, register, assignment]
#     if randint(0, 1) == 1:
#         timestamp = timestamp + randint(0, 100000)
#         assignment = AssignmentEvent(
#             public_uuid=register.public_uuid,
#             rubric_version_uuid=rubric.version_uuid,
#             name=rubric_names[randint(0, len(rubric_names) - 1)],
#             description=descriptions[randint(0, len(descriptions) - 1)],
#             version_timestamp=timestamp,
#         )
#         events.append(assignment)
#     return (events, assignment.public_uuid)


# def generate_dummy_data() -> list:
#     events = []

#     organizations_timestamp = {}
#     # Create some organizations
#     for _ in range(30):
#         # Create a random timestamp
#         timestamp = 1707133928 + randint(-100000, 100000)
#         uuid = str(uuid4())
#         org = OrganizationEvent(
#             public_uuid=uuid,
#             name=organization_names[randint(0, len(organization_names) - 1)],
#             version_timestamp=timestamp,
#         )
#         events.append(org)
#         organizations_timestamp[uuid] = timestamp

#         for _ in range(randint(0, 3)):
#             # Create a random timestamp which is greater than the organization timestamp
#             timestamp = timestamp + randint(0, 100000)
#             org = OrganizationEvent(
#                 public_uuid=uuid,
#                 name=organization_names[randint(0, len(organization_names) - 1)],
#                 version_timestamp=timestamp,
#             )
#             events.append(org)

#     # Create some instructors
#     instructors_org = {}
#     instructors_timestamp = {}
#     for _ in range(50):
#         # Select a random organization
#         org_uuid = list(organizations_timestamp.keys())[
#             randint(0, len(organizations_timestamp) - 1)
#         ]
#         timestamp = organizations_timestamp[org_uuid] + randint(0, 100000)

#         instructor_type = randint(1, 2)

#         registry = RegisterInstructorPublicUUIDEvent(
#             lms_id=str(randint(0, 100000000)),
#             user_type=instructor_type,
#             organization_public_uuid=org_uuid,
#         )
#         instructor = InstructorEvent(
#             public_uuid=registry.public_uuid,
#             name=instructor_names[randint(0, len(instructor_names) - 1)],
#             email=emails[randint(0, len(emails) - 1)],
#             version_timestamp=timestamp,
#         )
#         events.append(instructor)
#         instructors_org[registry.public_uuid] = org_uuid
#         instructors_timestamp[registry.public_uuid] = timestamp
#         events.append(registry)

#         for _ in range(0, 1):
#             timestamp = timestamp + randint(0, 100000)
#             instructor = InstructorEvent(
#                 public_uuid=registry.public_uuid,
#                 name=instructor_names[randint(0, len(instructor_names) - 1)],
#                 email=emails[randint(0, len(emails) - 1)],
#                 version_timestamp=timestamp,
#             )
#             events.append(instructor)

#     # Create some students
#     students_org = {}
#     students_timestamp = {}
#     for _ in range(1000):
#         # Select a random organization
#         org_uuid = list(organizations_timestamp.keys())[
#             randint(0, len(organizations_timestamp) - 1)
#         ]
#         timestamp = organizations_timestamp[org_uuid] + randint(0, 100000)

#         registry = RegisterStudentPublicUUIDEvent(
#             lms_id=str(randint(0, 100000000)),
#             organization_public_uuid=org_uuid,
#         )
#         student = StudentEvent(
#             public_uuid=registry.public_uuid,
#             name=instructor_names[randint(0, len(instructor_names) - 1)],
#             email=emails[randint(0, len(emails) - 1)],
#             version_timestamp=timestamp,
#         )
#         events.append(student)
#         students_org[registry.public_uuid] = org_uuid
#         students_timestamp[registry.public_uuid] = timestamp
#         events.append(registry)

#         for _ in range(0, 1):
#             timestamp = timestamp + randint(0, 100000)
#             student = StudentEvent(
#                 public_uuid=registry.public_uuid,
#                 name=instructor_names[randint(0, len(instructor_names) - 1)],
#                 email=emails[randint(0, len(emails) - 1)],
#                 version_timestamp=timestamp,
#             )
#             events.append(student)

#     # Create some courses
#     courses_instructors = {}
#     courses_timestamp = {}
#     for _ in range(100):
#         # Select a random instructor
#         instructor_uuid = list(instructors_timestamp.keys())[
#             randint(0, len(instructors_timestamp) - 1)
#         ]
#         timestamp = organizations_timestamp[instructors_org[instructor_uuid]] + randint(
#             0, 100000
#         )

#         registry = RegisterCoursePublicUUIDEvent(
#             lms_id=str(randint(0, 100000000)),
#             organization_public_uuid=instructors_org[instructor_uuid],
#         )
#         course = CourseEvent(
#             public_uuid=registry.public_uuid,
#             instructor_public_uuid=instructor_uuid,
#             name=course_names[randint(0, len(course_names) - 1)],
#             description=descriptions[randint(0, len(descriptions) - 1)],
#         )
#         events.append(course)
#         courses_instructors[registry.public_uuid] = instructor_uuid
#         courses_timestamp[registry.public_uuid] = timestamp
#         events.append(registry)

#         add_to_course_timestamp = instructors_timestamp[instructor_uuid] + randint(
#             0, 100000
#         )

#         add_instructor = InstructorAddedToCourseEvent(
#             instructor_public_uuid=instructor_uuid,
#             course_public_uuid=registry.public_uuid,
#             version_timestamp=add_to_course_timestamp,
#         )
#         events.append(add_instructor)

#         # Now, randomly maybe remove the instructor from the course and add a different one back on
#         if randint(0, 1) == 1:
#             remove_instructor = InstructorRemovedFromCourseEvent(
#                 instructor_public_uuid=instructor_uuid,
#                 course_public_uuid=registry.public_uuid,
#                 version_timestamp=add_to_course_timestamp + randint(0, 1000),
#             )
#             events.append(remove_instructor)

#             # Find all instructors in the same organization as the removed instructor
#             instructors_in_org = [
#                 instructor
#                 for instructor in instructors_org
#                 if instructors_org[instructor] == instructors_org[instructor_uuid]
#             ]
#             # Add a new instructor to the course
#             new_instructor = instructors_in_org[randint(0, len(instructors_in_org) - 1)]
#             add_instructor = InstructorAddedToCourseEvent(
#                 instructor_public_uuid=new_instructor,
#                 course_public_uuid=registry.public_uuid,
#                 version_timestamp=add_to_course_timestamp + randint(0, 1000),
#             )
#             events.append(add_instructor)

#         for _ in range(0, 1):
#             timestamp = timestamp + randint(0, 100000)
#             course = CourseEvent(
#                 public_uuid=registry.public_uuid,
#                 instructor_public_uuid=instructor_uuid,
#                 name=course_names[randint(0, len(course_names) - 1)],
#                 description=descriptions[randint(0, len(descriptions) - 1)],
#             )
#             events.append(course)

#     # Now, create a bunch of assignments
#     assignment_course = {}
#     for _ in range(1000):
#         # Select a random course and get the instructor
#         course_uuid = list(courses_timestamp.keys())[
#             randint(0, len(courses_timestamp) - 1)
#         ]
#         instructor_uuid = courses_instructors[course_uuid]
#         timestamp = courses_timestamp[course_uuid] + randint(0, 100000)

#         (assignment_events, assignment_uuid) = create_assignment(
#             instructors_org[instructor_uuid], instructor_uuid, timestamp
#         )
#         events.extend(assignment_events)
#         assignment_course[assignment_uuid] = course_uuid

#     # Now, create a bunch of sections
#     section_course = {}
#     for _ in range(50):
#         # Select a random course
#         course_uuid = list(courses_timestamp.keys())[
#             randint(0, len(courses_timestamp) - 1)
#         ]
#         timestamp = courses_timestamp[course_uuid] + randint(0, 100000)

#         registry = RegisterSectionPublicUUIDEvent(
#             lms_id=str(randint(0, 10000000)),
#             course_public_uuid=course_uuid,
#         )
#         section = SectionEvent(
#             public_uuid=registry.public_uuid,
#             course_public_uuid=course_uuid,
#             name=course_names[randint(0, len(course_names) - 1)],
#             version_timestamp=timestamp,
#         )
#         events.append(section)
#         section_course[registry.public_uuid] = course_uuid
#         events.append(registry)

#         for _ in range(0, 1):
#             timestamp = timestamp + randint(0, 100000)
#             section = SectionEvent(
#                 public_uuid=registry.public_uuid,
#                 course_public_uuid=course_uuid,
#                 name=course_names[randint(0, len(course_names) - 1)],
#                 version_timestamp=timestamp,
#             )
#             events.append(section)

#     # Now, assign students to sections
#     student_sections = {}
#     for student_id in students_org:
#         section_uuid = list(section_course.keys())[randint(0, len(section_course) - 1)]
#         timestamp = max(
#             students_timestamp[student_id], section_course[section_uuid]
#         ) + randint(0, 100000)
#         student_section = StudentAddedToSectionEvent(
#             student_public_uuid=student_id,
#             section_public_uuid=section_uuid,
#             version_timestamp=timestamp,
#         )
#         events.append(student_section)
#         student_sections[student_id] = section_uuid
#         if randint(0, 5) == 1:
#             timestamp = timestamp + randint(0, 100000)
#             student_section = StudentRemovedFromSectionEvent(
#                 student_public_uuid=student_id,
#                 section_public_uuid=section_uuid,
#                 version_timestamp=timestamp,
#             )
#             events.append(student_section)
#             student_sections.pop(student_id)

#     # Now, create some submissions
#     submissions = {}
#     for student_id in student_sections:
#         # Get the course for the section
#         course_uuid = section_course[student_sections[student_id]]
#         # Find all assignments for the course
#         assignments = [
#             assignment
#             for assignment in assignment_course
#             if assignment_course[assignment] == course_uuid
#         ]
#         for assignment_uuid in assignments:
#             submission_file_group = SubmissionFileGroupEvent(
#                 student_public_uuid=student_id,
#                 file_contents=[
#                     FileContent(
#                         "submission",
#                         "py",
#                         "Hello World",
#                     ),
#                     FileContent(
#                         "submission",
#                         "py",
#                         "Hello World",
#                     ),
#                 ],
#             )
#             events.append(submission_file_group)

#             timestamp = max(
#                 students_timestamp[student_id], courses_timestamp[course_uuid]
#             ) + randint(0, 100000)
#             registry = RegisterSubmissionPublicUUIDEvent(
#                 lms_id=str(randint(0, 100000000)),
#                 organization_public_uuid=students_org[student_id],
#             )
#             submission = SubmissionEvent(
#                 public_uuid=registry.public_uuid,
#                 student_public_uuid=student_id,
#                 assignment_public_uuid=assignment_uuid,
#                 submission_file_group_uuid=submission_file_group.uuid,
#                 version_timestamp=timestamp,
#             )
#             events.append(submission)
#             submissions[registry.public_uuid] = (student_id, assignment_uuid)
#             events.append(registry)

#             if randint(0, 1) == 1:
#                 timestamp = timestamp + randint(0, 100000)
#                 submission = SubmissionEvent(
#                     public_uuid=registry.public_uuid,
#                     student_public_uuid=student_id,
#                     assignment_public_uuid=assignment_uuid,
#                     submission_file_group_uuid=submission_file_group.uuid,
#                     version_timestamp=timestamp,
#                 )
#                 events.append(submission)
