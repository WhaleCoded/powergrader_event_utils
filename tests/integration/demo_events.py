from typing import List, Union, Tuple

import time

from powergrader_event_utils.events import (
    OrganizationEvent,
    InstructorEvent,
    RegisterInstructorPublicUUIDEvent,
    LMSInstructorType,
    CourseEvent,
    RegisterCoursePublicUUIDEvent,
    SectionEvent,
    RegisterSectionPublicUUIDEvent,
    StudentEvent,
    RegisterStudentPublicUUIDEvent,
    AssignmentEvent,
    RegisterAssignmentPublicUUIDEvent,
    RubricEvent,
    RegisterRubricPublicUUIDEvent,
    RubricCriterion,
    CriterionLevel,
    SubmissionEvent,
    RegisterSubmissionPublicUUIDEvent,
    SubmissionFileGroupEvent,
    FileContent,
    AICriterionGradingStartedEvent,
    AICriterionGradeEvent,
    Grade,
    AIInferredCriterionGradeEvent,
    InstructorOverrideCriterionGradeEvent,
    InstructorCriterionGradeEvent,
    InstructorAddedToCourseEvent,
    StudentAddedToSectionEvent,
    AssignmentAddedToCourseEvent,
)


def create_demo_events() -> list:
    events = []

    organization = create_demo_organization()
    events.append(organization)

    instructor_events, instructor_public_id = create_demo_instructor()
    events.extend(instructor_events)

    course_events, course_public_id = create_demo_course(instructor_public_id)
    events.extend(course_events)

    section_events, section_public_id = create_demo_section(course_public_id)
    events.extend(section_events)

    student_events, student_public_id = create_demo_student(section_public_id)
    events.extend(student_events)

    assignment_events, assignment_version_id = create_demo_assignment(
        instructor_public_id, course_public_id
    )
    events.extend(assignment_events)

    submission_events, submission_public_id = create_demo_submission(
        student_public_id, assignment_version_id
    )
    events.extend(submission_events)

    ai_grading_events, override_criterion_uuid = create_ai_grading_events(
        submission_public_id
    )
    events.extend(ai_grading_events)

    ai_inference_events = create_ai_inference_events(
        instructor_public_id, override_criterion_uuid, submission_public_id
    )
    events.extend(ai_inference_events)

    return events


def create_ai_inference_events(
    instructor_public_id: str,
    criterion_grade_version_uuid: str,
    submission_version_uuid: str,
) -> List[
    Union[
        AICriterionGradingStartedEvent,
        AIInferredCriterionGradeEvent,
        InstructorOverrideCriterionGradeEvent,
    ]
]:
    grade_override = InstructorOverrideCriterionGradeEvent(
        criterion_uuid="criterion-3",
        submission_version_uuid=submission_version_uuid,
        previous_criterion_grade_version_uuid=criterion_grade_version_uuid,
        instructor_public_uuid=instructor_public_id,
        grade=Grade(
            score=3,
            assessment="Program is organized well. There is no use of global state, and all behavior is contained in functions. Entrypoint is clearly defined and dunder main is used.",
        ),
    )
    return [grade_override]


def create_ai_grading_events(
    submission_version_uuid: str,
) -> Tuple[List[Union[AICriterionGradingStartedEvent, AICriterionGradeEvent]], str]:
    override_criterion_uuid = None
    events = []
    grading_started = AICriterionGradingStartedEvent(
        criterion_uuid="criterion-1",
        submission_version_uuid=submission_version_uuid,
        time_started=get_miliseconds_since_epoch(),
    )
    grading = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started.version_uuid,
        grading_method_uuid="tree-of-thoughts-001",
        grade=Grade(
            score=3,
            assessment="While invalid input throws errors that are caught, they immediatly end the program, which somewhat stretches the definition of 'The program does not error out for any user input.' For large numbers the program errors out when the recursion limit is reached, this is a very techinical issue, but it is fixable and the rubric says 'The program produces valid outputs for all valid inputs. Behavior is correct and complete.' is required for a 4. These two facts together give the rating a 3/4",
        ),
        time_finished=get_miliseconds_since_epoch(),
    )
    events.extend([grading_started, grading])

    grading_started = AICriterionGradingStartedEvent(
        criterion_uuid="criterion-2",
        submission_version_uuid=submission_version_uuid,
        time_started=get_miliseconds_since_epoch(),
    )
    grading = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started.version_uuid,
        grading_method_uuid="tree-of-thoughts-001",
        grade=Grade(
            score=3,
            assessment="Program implements the fibonacci sequence recursively, correctly starting at N=1.",
        ),
        time_finished=get_miliseconds_since_epoch(),
    )
    events.extend([grading_started, grading])

    grading_started = AICriterionGradingStartedEvent(
        criterion_uuid="criterion-3",
        submission_version_uuid=submission_version_uuid,
        time_started=get_miliseconds_since_epoch(),
    )
    grading = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started.version_uuid,
        grading_method_uuid="tree-of-thoughts-001",
        grade=Grade(
            score=2,
            assessment="Program displays decent organization. All behaviour is contained in functions.",
        ),
        time_finished=get_miliseconds_since_epoch(),
    )
    override_criterion_uuid = grading_started.criterion_uuid
    events.extend([grading_started, grading])

    grading_started = AICriterionGradingStartedEvent(
        criterion_uuid="criterion-4",
        submission_version_uuid=submission_version_uuid,
        time_started=get_miliseconds_since_epoch(),
    )
    grading = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started.version_uuid,
        grading_method_uuid="tree-of-thoughts-001",
        grade=Grade(
            score=3,
            assessment="Program contains good documentation. All functions have docstrings and comments are present where necessary. Docstrings are descriptive, and comments disambiguate code. There could be a few more comments inside of main(), and potentially a comment describing how the logic of the fibonacci calculator works for those who don't know, but these are so minor I will not dock points.",
        ),
        time_finished=get_miliseconds_since_epoch(),
    )
    events.extend([grading_started, grading])

    return events, override_criterion_uuid


def create_demo_submission(
    student_public_uuid: str,
    assignment_version_uuid: str,
) -> (
    List[
        Union[
            RegisterSubmissionPublicUUIDEvent,
            SubmissionEvent,
        ]
    ],
    str,
):
    submission_file_group = SubmissionFileGroupEvent(
        student_public_uuid=student_public_uuid,
        file_contents=[
            FileContent(
                file_name="fibonacci",
                file_type="py",
                content="""def fibonacci(n):
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
        main()""",
            )
        ],
    )

    register_submission = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id="7",
        lms_student_id="8",
        organization_public_uuid="ORGANIZATION-Apporto",
    )
    submission = SubmissionEvent(
        public_uuid=register_submission.public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group.uuid,
        version_timestamp=get_miliseconds_since_epoch(),
    )
    return (
        [submission_file_group, register_submission, submission],
        submission.public_uuid,
    )


def create_demo_assignment(
    instructor_public_uuid: str,
    course_public_uuid: str,
) -> Tuple[List[Union[RegisterAssignmentPublicUUIDEvent, AssignmentEvent]], str]:
    register_rubric = RegisterRubricPublicUUIDEvent(
        lms_id="5",
        organization_public_uuid="ORGANIZATION-Apporto",
    )
    rubric = RubricEvent(
        public_uuid=register_rubric.public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name="Fibonacci Sequence Rubric",
        rubric_criteria=[
            RubricCriterion(
                uuid="criterion-1",
                name="Functionality",
                levels=[
                    CriterionLevel(
                        score=0,
                        description="The program does not run due to syntax errors. Behavior is entirely incorrect or incomplete.",
                    ),
                    CriterionLevel(
                        score=1,
                        description="The program runs, but will throw uncaught errors. Behavior is significantly incorrect or incomplete.",
                    ),
                    CriterionLevel(
                        score=2,
                        description="The program runs, but will throw uncaught errors for valid user input. The program may contain significant behavior errors.",
                    ),
                    CriterionLevel(
                        score=3,
                        description="The program runs and will only error out when given invalid user input. The program may have some unexpected behavior.",
                    ),
                    CriterionLevel(
                        score=4,
                        description="The program does not error out for any user input. The program produces valid outputs for all valid inputs. Behavior is correct and complete.",
                    ),
                ],
            ),
            RubricCriterion(
                uuid="criterion-2",
                name="Requirements",
                levels=[
                    CriterionLevel(
                        score=0,
                        description="Program does not implement the fibonacci sequence. No recursion is present.",
                    ),
                    CriterionLevel(
                        score=1,
                        description="Program is missing either the fibonacci sequence or recursion.",
                    ),
                    CriterionLevel(
                        score=2,
                        description="Program implements the fibonacci sequence recursively, but does not start at N=1.",
                    ),
                    CriterionLevel(
                        score=3,
                        description="Program implements the fibonacci sequence recursively, correctly starting at N=1.",
                    ),
                ],
            ),
            RubricCriterion(
                uuid="criterion-3",
                name="Organization",
                levels=[
                    CriterionLevel(
                        score=0,
                        description="Program contains no attempt at organization. Significant use of global state. Behavior may not be contained in functions.",
                    ),
                    CriterionLevel(
                        score=1,
                        description="Program has very poor organization. Some use of global state. Most behavior is contained in functions.",
                    ),
                    CriterionLevel(
                        score=2,
                        description="Program displays decent organization. There is minimal use of global state, and all behavior is contained in functions.",
                    ),
                    CriterionLevel(
                        score=3,
                        description="Program is organized well. There is no use of global state, and all behavior is contained in functions. Entrypoint is clearly defined and dunder main is used.",
                    ),
                ],
            ),
            RubricCriterion(
                uuid="criterion-4",
                name="Documentation",
                levels=[
                    CriterionLevel(
                        score=0,
                        description="Program contains no documentation. No docstrings or comments are present.",
                    ),
                    CriterionLevel(
                        score=1,
                        description="Program contains minimal documentation. Some docstrings or comments are present.",
                    ),
                    CriterionLevel(
                        score=2,
                        description="Program contains decent documentation. All functions have docstrings and comments are present where necessary.",
                    ),
                    CriterionLevel(
                        score=3,
                        description="Program contains good documentation. All functions have docstrings and comments are present where necessary. Docstrings are descriptive, and comments disambiguate code.",
                    ),
                ],
            ),
        ],
        version_timestamp=get_miliseconds_since_epoch(),
    )

    register_assignment = RegisterAssignmentPublicUUIDEvent(
        lms_id="6",
        organization_public_uuid="ORGANIZATION-Apporto",
    )
    assignment = AssignmentEvent(
        public_uuid=register_assignment.public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric.version_uuid,
        name="Assignment 1",
        description="""Assignment 4: Recursion

    Write a Python program to get the Fibonacci number at N.

    Note : The Fibonacci Sequence is the series of numbers :
    0, 1, 1, 2, 3, 5, 8, 13, 21, ....
    Every next number is found by adding up the two numbers before it.

    Remember to implement your solution using recursion.
    The final program should take user input from the terminal specifying the desired Fibonacci number and display the calculated result.
    (Note: The first entry is N=1)""",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    add_assignment_to_course = AssignmentAddedToCourseEvent(
        assignment_public_uuid=assignment.public_uuid,
        course_public_uuid=course_public_uuid,
        timestamp=get_miliseconds_since_epoch(),
    )
    return [
        register_assignment,
        assignment,
        add_assignment_to_course,
    ], assignment.version_uuid


def create_demo_student(
    section_public_uuid: str,
) -> Tuple[List[Union[RegisterStudentPublicUUIDEvent, StudentEvent]], str]:
    register_student = RegisterStudentPublicUUIDEvent(
        lms_id="4",
        organization_public_uuid="ORGANIZATION-Apporto",
    )
    student = StudentEvent(
        public_uuid=register_student.public_uuid,
        name="Jerry Smith",
        email="jerry.smith@gmail.com",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    register_student_for_section = StudentAddedToSectionEvent(
        student_public_uuid=student.public_uuid,
        section_public_uuid=section_public_uuid,
        timestamp=get_miliseconds_since_epoch(),
    )
    return (
        [register_student, student, register_student_for_section],
        student.public_uuid,
    )


def create_demo_section(
    course_public_uuid: str,
) -> Tuple[List[Union[RegisterSectionPublicUUIDEvent, SectionEvent]], str]:
    register_section = RegisterSectionPublicUUIDEvent(
        lms_id="3",
        organization_public_uuid="ORGANIZATION-Apporto",
    )
    section = SectionEvent(
        public_uuid=register_section.public_uuid,
        course_public_uuid=course_public_uuid,
        name="Monday 10:00 AM",
        closed=False,
        version_timestamp=get_miliseconds_since_epoch(),
    )
    return [register_section, section], section.public_uuid


def create_demo_course(
    instructor_public_id: str,
) -> Tuple[List[Union[RegisterCoursePublicUUIDEvent, CourseEvent]], str]:
    register_course = RegisterCoursePublicUUIDEvent(
        lms_id="2",
        organization_public_uuid="ORGANIZATION-Apporto",
    )
    course = CourseEvent(
        public_uuid=register_course.public_uuid,
        instructor_public_uuid=instructor_public_id,
        name="Introduction to Computer Science",
        description="This course is an introduction to computer science.",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    instructor_added_to_course = InstructorAddedToCourseEvent(
        course_public_uuid=course.public_uuid,
        instructor_public_uuid=instructor_public_id,
        timestamp=get_miliseconds_since_epoch(),
    )
    return [register_course, course, instructor_added_to_course], course.public_uuid


def create_demo_instructor() -> (
    Tuple[List[Union[RegisterInstructorPublicUUIDEvent, InstructorEvent]], str]
):
    register_instructor = RegisterInstructorPublicUUIDEvent(
        lms_id="1",
        user_type=LMSInstructorType.FACULTY,
        organization_public_uuid="ORGANIZATION-Apporto",
    )
    instructor = InstructorEvent(
        public_uuid=register_instructor.public_uuid,
        name="Professor Smith",
        email="drsmith@apporto.com",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    return ([register_instructor, instructor], instructor.public_uuid)


def create_demo_organization() -> OrganizationEvent:
    return OrganizationEvent(
        public_uuid="ORGANIZATION-Apporto",
        name="Apporto",
        version_timestamp=get_miliseconds_since_epoch(),
    )


def get_miliseconds_since_epoch():
    return int(time.time_ns() / 1_000_000)


if __name__ == "__main__":
    events = create_demo_events()
    for event in events:
        print(event)
