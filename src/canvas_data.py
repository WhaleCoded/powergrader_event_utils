



from asyncio import Event
from typing import List

from powergrader_event_utils.events import (
    RubricEvent,
    AssignmentEvent,
    SubmissionEvent,
    InstructorOverrideCriterionGradeEvent,
    InstructorCriterionGradeEvent,
    Grade,
    RubricCriterion as EventRubricCriterion,
    CriterionLevel as EventCriterionLevel,
    CourseEvent
)
from powergrader_event_utils.events.course import OrganizationEvent
from powergrader_event_utils.events.publish import (
    RegisterCoursePublicUUIDEvent, 
    RegisterInstructorPublicUUIDEvent, 
    RegisterSectionPublicUUIDEvent, 
    RegisterStudentPublicUUIDEvent,
    RegisterAssignmentPublicUUIDEvent,
    RegisterRubricPublicUUIDEvent,
    RegisterSubmissionPublicUUIDEvent,
)

def canvas_data_as_events() -> List[Event]:

    events_to_send = []
    org_uuid = "463bffc1-cd43-466a-9b15-49921b2c384f"

    # ORG
    register_org_event: OrganizationEvent = OrganizationEvent(public_uuid=org_uuid, name="Canvas/Apporto Test Data")
    events_to_send.append(register_org_event)

    # COURSE
    register_course_event: RegisterCoursePublicUUIDEvent = RegisterCoursePublicUUIDEvent(lms_id="264", organization_public_uuid=org_uuid)
    events_to_send.append(register_course_event)

    # SECTION
    register_section_event: RegisterSectionPublicUUIDEvent = RegisterSectionPublicUUIDEvent(lms_id="306", organization_public_uuid=org_uuid)
    events_to_send.append(register_section_event)
    
    # INSTRUCTOR
    register_instructor_event: RegisterInstructorPublicUUIDEvent = RegisterInstructorPublicUUIDEvent(lms_id="123", user_type=2, organization_public_uuid=org_uuid)
    events_to_send.append(register_instructor_event)

    # STUDENTS
    for student_id in ["343", "344", "345", "346", "347"]:
        register_student_event: RegisterStudentPublicUUIDEvent = RegisterStudentPublicUUIDEvent(lms_id=student_id, organization_public_uuid=org_uuid)
        events_to_send.append(register_student_event)

    # ASSIGNMENTS
    for assignment_id in ["272", "273", "274"]:
        register_assignment_event: RegisterAssignmentPublicUUIDEvent = RegisterAssignmentPublicUUIDEvent(lms_id=assignment_id, organization_public_uuid=org_uuid)
        events_to_send.append(register_assignment_event)

    # RUBRICS
    for rubric_id in ["109", "110", "111"]:
        register_rubric_event: RegisterRubricPublicUUIDEvent = RegisterRubricPublicUUIDEvent(lms_id=rubric_id, organization_public_uuid=org_uuid)
        events_to_send.append(register_rubric_event)

    return events_to_send