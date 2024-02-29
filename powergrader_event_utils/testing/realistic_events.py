import os
import json
from typing import List
from uuid import uuid4
from random import randint, choice

from powergrader_event_utils.events import *

FIRST_NAMES = [
    "John",
    "Maria",
    "Michael",
    "Samantha",
    "David",
    "Emily",
    "Daniel",
    "Emma",
    "Lily",
    "Olivia",
    "Jose",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Jones",
    "Brown",
    "Davis",
    "Miller",
    "Wilson",
    "Moore",
    "Taylor",
]


def create_realistic_events_from_jsonl_test_output(
    jsonl_file_path: str,
) -> List[PowerGraderEvent]:
    # Get the parent directory of the jsonl file
    grading_method_uuid = os.path.dirname(jsonl_file_path)

    with open(jsonl_file_path, "r") as f:
        lines = f.readlines()

    trial_info = []
    assignmnet_info = {}
    student_ids = {}
    student_levels = set()
    assignment_difficulties = set()
    for line in lines:
        temp_info = json.loads(line)

        if (
            "student_id" in temp_info
            and "student_level" in temp_info
            and "assignment_difficulty" in temp_info
            and "method_output" in temp_info
            and "example" in temp_info
            and temp_info["student_level"] is not None
        ):
            student_ids[temp_info["student_id"]] = temp_info["student_level"]
            student_levels.add(temp_info["student_level"])
            assignment_difficulties.add(temp_info["assignment_difficulty"])
            trial_info.append(temp_info)

        if (
            "assignment_name" in temp_info
            and "example" in temp_info
            and "assignment_difficulty" in temp_info
        ):
            assignmnet_info[temp_info["assignment_name"]] = {
                "difficulty": temp_info["assignment_difficulty"],
                "rubric": temp_info["example"]["rubric"],
                "description": temp_info["example"]["assignment"],
            }

    # Gather all the events
    events = []

    # Create the organization event
    org_event = OrganizationEvent(
        public_uuid=str(uuid4()),
        name="Apporto Test",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events.append(org_event)
    print("1 - Organization Event Created")

    # Create instructor event
    register_instructor_event = RegisterInstructorPublicUUIDEvent(
        lms_id=str(randint(1, 1_000_000)),
        organization_public_uuid=org_event.public_uuid,
        user_type=LMSInstructorType.FACULTY,
    )
    instructor_event = InstructorEvent(
        public_uuid=register_instructor_event.public_uuid,
        name="Dallin Hutchison",
        email="d.hutchison@apporto.com",
        version_timestamp=get_miliseconds_since_epoch(),
    )
    events.append(register_instructor_event)
    events.append(instructor_event)
    print("1 Instructor Event Created")

    # Create a course for each assignment difficulty
    course_events = {}
    section_events = {}
    num_sections = 0
    for difficulty in assignment_difficulties:
        difficulty: str

        register_course_event = RegisterCoursePublicUUIDEvent(
            lms_id=str(randint(1, 1_000_000)),
            organization_public_uuid=org_event.public_uuid,
        )
        course_event = CourseEvent(
            public_uuid=register_course_event.public_uuid,
            name=f"{difficulty.upper()} Python",
            instructor_public_uuid=instructor_event.public_uuid,
            description=f"A course to teach {difficulty.upper()} Python concepts.",
            version_timestamp=get_miliseconds_since_epoch(),
        )
        instructor_added_to_course_event = InstructorAddedToCourseEvent(
            instructor_public_uuid=instructor_event.public_uuid,
            course_public_uuid=course_event.public_uuid,
            timestamp=get_miliseconds_since_epoch(),
        )
        events.append(register_course_event)
        events.append(course_event)
        events.append(instructor_added_to_course_event)
        course_events[difficulty] = course_event

        # Create sections for each student level
        for level in student_levels:
            level: str

            register_section_event = RegisterSectionPublicUUIDEvent(
                lms_id=str(randint(1, 1_000_000)),
                organization_public_uuid=org_event.public_uuid,
            )
            section_event = SectionEvent(
                public_uuid=register_section_event.public_uuid,
                name=f"Section {level.upper()}",
                course_public_uuid=course_event.public_uuid,
                closed=False,
                version_timestamp=get_miliseconds_since_epoch(),
            )
            events.append(register_section_event)
            events.append(section_event)

            if difficulty not in section_events:
                section_events[difficulty] = {}
            section_events[difficulty][level] = section_event
            num_sections += 1
    print(f"{len(course_events.keys())} Course Events Created")
    print(f"{num_sections} Section Events Created")

    # Create student events and add them to the appropriate section
    student_events = {}
    register_student_events = {}
    for student_id, student_level in student_ids.items():
        first_name = choice(FIRST_NAMES)
        last_name = choice(LAST_NAMES)

        register_student_event = RegisterStudentPublicUUIDEvent(
            lms_id=str(randint(1, 1_000_000)),
            organization_public_uuid=org_event.public_uuid,
        )
        student_event = StudentEvent(
            public_uuid=register_student_event.public_uuid,
            name=f"{first_name} {last_name}",
            email=f"{first_name.lower()}.{last_name.lower()}@apporto.com",
            version_timestamp=get_miliseconds_since_epoch(),
        )
        events.append(register_student_event)
        events.append(student_event)
        student_events[student_id] = student_event
        register_student_events[student_id] = register_student_event

        # Add the student to each of the appropriate sections
        for difficulty in assignment_difficulties:
            difficulty: str
            section_event: SectionEvent = section_events[difficulty][student_level]

            student_added_to_section_event = StudentAddedToSectionEvent(
                student_public_uuid=student_event.public_uuid,
                section_public_uuid=section_event.public_uuid,
                timestamp=get_miliseconds_since_epoch(),
            )
            events.append(student_added_to_section_event)
    print(f"{len(student_events.keys())} Student Events Created")

    # Create assignment events
    assignment_events = {}
    register_assignment_events = {}
    rubric_events = {}
    for assignment_name, info in assignmnet_info.items():
        assignment_name: str
        difficulty = info["difficulty"]
        description = info["description"]
        rubric = info["rubric"]

        # Format the criteria for the rubric
        formatted_rubric_criteria = []
        for criterion in rubric:
            levels = []
            for level in criterion["levels"]:
                levels.append(
                    CriterionLevel(
                        description=level["description"],
                        score=level["score"],
                    )
                )

            formatted_rubric_criteria.append(
                RubricCriterion(name=criterion["name"], levels=levels)
            )

        register_rubric_event = RegisterRubricPublicUUIDEvent(
            lms_id=str(randint(1, 1_000_000)),
            organization_public_uuid=org_event.public_uuid,
        )
        rubric_event = RubricEvent(
            public_uuid=register_rubric_event.public_uuid,
            instructor_public_uuid=instructor_event.public_uuid,
            name=f"{assignment_name.upper()} Rubric",
            rubric_criteria=formatted_rubric_criteria,
            version_timestamp=get_miliseconds_since_epoch(),
        )
        events.append(register_rubric_event)
        events.append(rubric_event)

        register_assignment_event = RegisterAssignmentPublicUUIDEvent(
            lms_id=str(randint(1, 1_000_000)),
            organization_public_uuid=org_event.public_uuid,
        )
        assignment_event = AssignmentEvent(
            public_uuid=register_assignment_event.public_uuid,
            instructor_public_uuid=instructor_event.public_uuid,
            rubric_version_uuid=rubric_event.version_uuid,
            name=assignment_name,
            description=description,
            version_timestamp=get_miliseconds_since_epoch(),
        )
        events.append(register_assignment_event)
        events.append(assignment_event)
        assignment_events[assignment_name] = assignment_event
        register_assignment_events[assignment_name] = register_assignment_event
        rubric_events[assignment_name] = rubric_event

        # Add the assignment to the appropriate course
        course_event: CourseEvent = course_events[difficulty]
        assignment_added_to_course_event = AssignmentAddedToCourseEvent(
            assignment_public_uuid=assignment_event.public_uuid,
            course_public_uuid=course_event.public_uuid,
            timestamp=get_miliseconds_since_epoch(),
        )
        events.append(assignment_added_to_course_event)
    print(f"{len(assignment_events.keys())} Assignment Events Created")
    print(f"{len(rubric_events.keys())} Rubric Events Created")

    # Create submission and grade events
    submission_handled_markers = set()
    num_ai_grades = 0
    num_instructor_grades = 0
    num_mismatched_inst_grades = 0
    num_mismiated_ai_grades = 0
    for trial in trial_info:
        assignmnet_name = trial["assignment_name"]
        student_level = trial["student_level"]
        student_id = trial["student_id"]
        method_output = trial["method_output"]
        example = trial["example"]
        example_id = trial["example_id"]

        # Create the submission event
        if example_id not in submission_handled_markers:
            assignment_event: AssignmentEvent = assignment_events[assignmnet_name]
            register_assignment_event: RegisterAssignmentPublicUUIDEvent = (
                register_assignment_events[assignmnet_name]
            )
            register_student_event: RegisterStudentPublicUUIDEvent = (
                register_student_events[student_id]
            )
            rubric_event: RubricEvent = rubric_events[assignmnet_name]

            register_submission_event = RegisterSubmissionPublicUUIDEvent(
                lms_assignment_id=register_assignment_event.lms_id,
                lms_student_id=register_student_event.lms_id,
                organization_public_uuid=org_event.public_uuid,
            )
            submission_file_group_event = SubmissionFileGroupEvent(
                student_public_uuid=register_student_event.public_uuid,
                file_contents=[
                    FileContent(
                        file_name="main",
                        file_type="py",
                        content=bytes(example["submission"], "utf-8"),
                    )
                ],
            )
            submission_event = SubmissionEvent(
                public_uuid=register_submission_event.public_uuid,
                student_public_uuid=register_student_event.public_uuid,
                assignment_version_uuid=assignment_event.version_uuid,
                submission_file_group_uuid=submission_file_group_event.uuid,
                version_timestamp=get_miliseconds_since_epoch(),
            )
            events.append(register_submission_event)
            events.append(submission_file_group_event)
            events.append(submission_event)
            submission_handled_markers.add(example_id)

            # Create the corresponding grade events for AI and Instructor
            for criterion_name, criterion in rubric_event.rubric_criteria.items():
                criterion_name: str
                criterion: RubricCriterion
                possible_scores = set([level.score for level in criterion.levels])

                instructor_grade_assesment = None
                instructor_grade_score = None
                for instructor_grade in example["grade"]:
                    if instructor_grade["name"] == criterion_name:
                        instructor_grade_assesment = instructor_grade["assessment"]
                        instructor_grade_score = int(instructor_grade["score"])
                        if instructor_grade_score not in possible_scores:
                            num_mismatched_inst_grades += 1
                            # Choose the closest score
                            instructor_grade_score = min(
                                possible_scores,
                                key=lambda x: abs(x - instructor_grade_score),
                            )
                        break

                if instructor_grade_assesment is None or instructor_grade_score is None:
                    raise ValueError("Could not find instructor grade for criterion")

                model_grade_assesment = None
                model_grade_score = None
                for model_grade in method_output:
                    if model_grade["name"] == criterion_name:
                        model_grade_assesment = model_grade["assessment"]
                        model_grade_score = int(model_grade["score"])
                        if model_grade_score not in possible_scores:
                            num_mismiated_ai_grades += 1
                            # Choose the closest score
                            model_grade_score = min(
                                possible_scores,
                                key=lambda x: abs(x - model_grade_score),
                            )
                        break

                if model_grade_assesment is None or model_grade_score is None:
                    raise ValueError("Could not find model grade for criterion")

                ai_grading_started_event = AICriterionGradingStartedEvent(
                    criterion_uuid=criterion.uuid,
                    submission_version_uuid=submission_event.version_uuid,
                    time_started=get_miliseconds_since_epoch(),
                )
                ai_criterion_grade_event = AICriterionGradeEvent(
                    grading_started_version_uuid=ai_grading_started_event.version_uuid,
                    grading_method_uuid=grading_method_uuid,
                    grade=Grade(
                        score=model_grade_score, assessment=model_grade_assesment
                    ),
                    time_finished=get_miliseconds_since_epoch(),
                )
                events.append(ai_grading_started_event)
                events.append(ai_criterion_grade_event)
                num_ai_grades += 1

                if instructor_grade_score != model_grade_score:
                    instructor_grade_event = InstructorCriterionGradeEvent(
                        criterion_uuid=criterion.uuid,
                        submission_version_uuid=submission_event.version_uuid,
                        instructor_public_uuid=instructor_event.public_uuid,
                        grade=Grade(
                            score=instructor_grade_score,
                            assessment=instructor_grade_assesment,
                        ),
                    )
                    events.append(instructor_grade_event)
                    num_instructor_grades += 1

    print(f"{len(submission_handled_markers)} Submission Events Created")
    print(f"{num_mismiated_ai_grades} Mismatched AI Grade Events Created")
    print(f"{num_ai_grades} AI Grade Events Created")
    print(f"{num_mismatched_inst_grades} Mismatched Instructor Grade Events Created")
    print(f"{num_instructor_grades} Instructor Grade Events Created")
    print(f"Total Grades: {num_ai_grades + num_instructor_grades}")
    print(f"Total Events: {len(events)}")

    return events
