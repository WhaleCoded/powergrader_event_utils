import random

from powergrader_event_utils.events import (
    RegisterInstructorPublicUUIDEvent,
    OrganizationEvent,
    CourseEvent,
    RubricEvent,
    RegisterCoursePublicUUIDEvent,
    RegisterStudentPublicUUIDEvent,
    RegisterSectionPublicUUIDEvent,
    SectionEvent,
    StudentAddedToSectionEvent,
    InstructorAddedToCourseEvent,
    AssignmentAddedToCourseEvent,
    RegisterAssignmentPublicUUIDEvent,
    AssignmentEvent,
    PublishedToLMSEvent,
    RegisterSubmissionPublicUUIDEvent,
    SubmissionEvent,
    FileContent,
    SubmissionFileGroupEvent,
)

from tqdm import tqdm


def rag_demo_publish(events_to_send, producer, slow=False):
    """Publish RAG events to Kafka."""

    # Find the instructor public UUID
    instructor_public_uuid = None
    organization_public_uuid = None
    rubric_event = None
    student_public_uuids = []
    student_lms_ids = []
    for event in events_to_send:
        if isinstance(event, RegisterInstructorPublicUUIDEvent):
            instructor_public_uuid = event.public_uuid
        elif isinstance(event, OrganizationEvent):
            organization_public_uuid = event.public_uuid
        elif isinstance(event, RubricEvent):
            rubric_event = event
        elif isinstance(event, RegisterStudentPublicUUIDEvent):
            student_public_uuids.append(event.public_uuid)
            student_lms_ids.append(event.lms_id)

    demo_setup_events = []
    reg_course_event = RegisterCoursePublicUUIDEvent(
        str(random.randint(0, 1000000)), organization_public_uuid
    )
    tes_course = CourseEvent(
        reg_course_event.public_uuid,
        instructor_public_uuid,
        "RAG Demo",
        "RAG Demo Course",
    )
    inst_added_event = InstructorAddedToCourseEvent(
        instructor_public_uuid, tes_course.public_uuid
    )
    demo_setup_events.append(reg_course_event)
    demo_setup_events.append(tes_course)
    demo_setup_events.append(inst_added_event)

    reg_section_event = RegisterSectionPublicUUIDEvent(
        str(random.randint(0, 1000000)), organization_public_uuid
    )
    tes_section = SectionEvent(
        reg_section_event.public_uuid, tes_course.public_uuid, "RAG Demo Section", False
    )
    demo_setup_events.append(reg_section_event)
    demo_setup_events.append(tes_section)

    for student_public_uuid in student_public_uuids[:3]:
        student_added_event = StudentAddedToSectionEvent(
            student_public_uuid, tes_section.public_uuid
        )
        demo_setup_events.append(student_added_event)

    reg_assignment_event = RegisterAssignmentPublicUUIDEvent(
        str(random.randint(0, 1000000)), organization_public_uuid
    )
    tes_assignment = AssignmentEvent(
        reg_assignment_event.public_uuid,
        instructor_public_uuid,
        rubric_event.version_uuid,
        "RAG Demo Assignment",
        "RAG Demo Assignment Description",
    )
    assignment_added_event = AssignmentAddedToCourseEvent(
        tes_assignment.public_uuid, tes_course.public_uuid
    )
    demo_setup_events.append(reg_assignment_event)
    demo_setup_events.append(tes_assignment)
    demo_setup_events.append(assignment_added_event)

    one_at_a_time_events = []
    publish = PublishedToLMSEvent(tes_assignment.version_uuid)
    one_at_a_time_events.append(publish)
    reg_sub_1 = RegisterSubmissionPublicUUIDEvent(
        reg_assignment_event.lms_id,
        student_lms_ids[0],
        organization_public_uuid,
    )
    file_content_1 = """
    def fibonacci(n):
        sequence = [0, 1]
        while len(sequence) < n:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[:n]

    # Example usage:
    n = 10
    print(f"First {n} numbers in the Fibonacci sequence: {fibonacci(n)}")
"""
    file_group_1 = SubmissionFileGroupEvent(
        student_public_uuids[0],
        [FileContent("test", ".py", bytes(file_content_1, "utf-8"))],
    )
    sub_1 = SubmissionEvent(
        reg_sub_1.public_uuid,
        student_public_uuids[0],
        tes_assignment.version_uuid,
        file_group_1.uuid,
    )
    # one_at_a_time_events.append([reg_sub_1, file_group_1, sub_1])
    demo_setup_events.append(reg_sub_1)
    demo_setup_events.append(file_group_1)
    demo_setup_events.append(sub_1)
    reg_sub_2 = RegisterSubmissionPublicUUIDEvent(
        reg_assignment_event.lms_id,
        student_lms_ids[1],
        organization_public_uuid,
    )
    file_content_2 = """
    def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

    # Example usage:
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Sorted array: {bubble_sort(arr)}")
    """
    file_group_2 = SubmissionFileGroupEvent(
        student_public_uuids[1],
        [FileContent("test", ".py", bytes(file_content_2, "utf-8"))],
    )
    sub_2 = SubmissionEvent(
        reg_sub_2.public_uuid,
        student_public_uuids[1],
        tes_assignment.version_uuid,
        file_group_2.uuid,
    )
    one_at_a_time_events.append([reg_sub_2, file_group_2, sub_2])

    reg_sub_3 = RegisterSubmissionPublicUUIDEvent(
        reg_assignment_event.lms_id,
        student_lms_ids[2],
        organization_public_uuid,
    )
    file_content_3 = """
        def is_palindrome(s):
            return s == s[::-1]

        # Example usage:
        string = "racecar"
        print(f"Is '{string}' a palindrome? {is_palindrome(string)}")
    """
    file_group_3 = SubmissionFileGroupEvent(
        student_public_uuids[2],
        [FileContent("test", ".py", bytes(file_content_3, "utf-8"))],
    )
    sub_3 = SubmissionEvent(
        reg_sub_3.public_uuid,
        student_public_uuids[2],
        tes_assignment.version_uuid,
        file_group_3.uuid,
    )
    one_at_a_time_events.append([reg_sub_3, file_group_3, sub_3])

    print("Sending the realistic events")
    for event in tqdm(events_to_send):
        event.publish(producer)
    producer.flush()

    print("Sending the rag_demo events")
    for event in tqdm(demo_setup_events):
        event.publish(producer)
    producer.flush()

    print("Sending the one_at_a_time events")
    for events in one_at_a_time_events:
        input("Press enter to send the next event")
        if isinstance(events, list):
            for event in tqdm(events):
                event.publish(producer)
        else:
            events.publish(producer)

        producer.flush()

    print("All events sent. Exiting.")
