def test_get_kafka_topic_name_for_event_type():
    from powergrader_event_utils.events.event import get_kafka_topic_name_for_event_type
    from powergrader_event_utils.events.event import EventType

    assert (
        get_kafka_topic_name_for_event_type(EventType.AI_CRITERION_GRADING_STARTED)
        == "AICriterionGradingStarted"
    )
    assert (
        get_kafka_topic_name_for_event_type(EventType.GRADING_METHOD) == "GradingMethod"
    )
    assert (
        get_kafka_topic_name_for_event_type(EventType.NOT_SPECIFIED) == "DOES_NOT_EXIST"
    )
    assert get_kafka_topic_name_for_event_type(EventType.RETRY) == "Retry"
    assert get_kafka_topic_name_for_event_type(EventType.STUDENT) == "Student"


def test_get_kafka_topic_names_for_event_types():
    from powergrader_event_utils.events.event import (
        get_kafka_topic_names_for_event_types,
    )

    event_types_output = get_kafka_topic_names_for_event_types()

    for string in [
        "Assignment",
        "Rubric",
        "Course",
        "Section",
        "Organization",
        "Retry",
        "DeadLetter",
        "AICriterionGradingStarted",
        "GradingMethod",
        "AICriterionGrade",
        "AIInferredCriterionGrade",
        "InstructorCriterionGrade",
        "InstructorOverrideCriterionGrade",
        "CriterionGradeEmbedding",
        "InstructorSubmissionGradeApproval",
        "RegisterCoursePublicUUID",
        "RegisterSectionPublicUUID",
        "RegisterInstructorPublicUUID",
        "RegisterStudentPublicUUID",
        "RegisterAssignmentPublicUUID",
        "RegisterRubricPublicUUID",
        "RegisterSubmissionPublicUUID",
        "PublishedToLMS",
        "PublishedGradeToLMS",
        "AssignmentAddedToCourse",
        "AssignmentRemovedFromCourse",
        "StudentAddedToSection",
        "StudentRemovedFromSection",
        "InstructorAddedToCourse",
        "InstructorRemovedFromCourse",
        "Submission",
        "SubmissionFileGroup",
        "Student",
        "Instructor",
    ]:
        assert string in event_types_output


def test_generate_event_uuid():
    from powergrader_event_utils.events.event import generate_event_uuid

    assert "Course--" in generate_event_uuid("CourseEvent")
    assert "Assignment--" in generate_event_uuid("AssignmentEvent")
    assert "Section--" in generate_event_uuid("SectionEvent")
    assert "Organization--" in generate_event_uuid("OrganizationEvent")
    assert "Retry--" in generate_event_uuid("RetryEvent")
    assert "DeadLetter--" in generate_event_uuid("DeadLetterEvent")
    assert "AICriterionGradingStarted--" in generate_event_uuid(
        "AICriterionGradingStartedEvent"
    )


def test_get_event_type_from_uuid():
    from powergrader_event_utils.events.event import get_event_type_from_uuid, EventType

    assert get_event_type_from_uuid("Course--") == EventType.COURSE
    assert get_event_type_from_uuid("Assignment--") == EventType.ASSIGNMENT
    assert get_event_type_from_uuid("Section--") == EventType.SECTION
    assert get_event_type_from_uuid("Organization--") == EventType.ORGANIZATION
    assert get_event_type_from_uuid("Retry--") == EventType.RETRY
    assert get_event_type_from_uuid("DeadLetter--") == EventType.DEAD_LETTER
