from typing import List, Union

import random

from powergrader_event_utils.events import (
    CourseEvent,
    RegisterCoursePublicUUIDEvent,
    RegisterSectionPublicUUIDEvent,
    SectionEvent,
    OrganizationEvent,
)

from utils import (
    generate_random_timestamp,
    generate_random_uuid,
    select_from_string_list,
)

COURSE_NAMES = [
    "CS 101",
    "Macro Biology",
    "Intro to Python",
    "History of Central East Asia",
    "Intro to Calculus",
    "BIO 3050",
    "CS 102",
]

COURSE_DESCRIPTIONS = [
    "This is a description",
    "This is an even longer description",
    "And this is a description which defies all expectations of length. In fact, it is so long that it is hard to believe that it is a description at all. It is more like a novel. A novel about a description. A description novel. A descriptovel.",
    "There once was a description from Nantucket, whose length was so long it could not be",
    "This course is about the history of the world. It is a very long course, and it is very difficult. You will learn a lot, but you will also have to work very hard. It is not for the faint of heart.",
    "An introduction to the world of computer science. This course will teach you the basics of programming, and will prepare you for more advanced courses in the future.",
    "Advanced inter-cellular biology. This course will teach you about the inner workings of cells, and how they interact with each other. General cellular dynamics will be covered, as well as the latest research in the field.",
    "This course is a continuation of CS 101. It will cover more advanced topics, and will prepare you for more advanced courses in the future.",
    "This course is a continuation of BIO 3050. It will cover more advanced topics, and will prepare you for more advanced courses in the future.",
    "Enter the world of linear algebra.",
    "Differential equations and their applications. Prerequisites: Calculus I and II.",
]

SECTION_NAMES = [
    "Section 1",
    "Section 2",
    "Section 3",
    "Section 4",
    "Section 5",
    "Section 6",
    "Section 7",
    "Section 8",
    "Morning Section",
    "Afternoon Section",
    "Evening Section",
    "Section A",
    "Section B",
    "Section C",
    "Section D",
    "Section E",
    "Section F",
    "Section G",
    "Section H",
    "Section I",
    "Section 101",
    "Section 102",
    "Section 103",
    "Section 104",
    "Section 105",
    "Section 106",
    "Section 107",
    "Section 108",
    "Section 10.1",
    "Section 10.2",
    "Section 10.3",
    "Section 10.4",
    "Section 10.5",
    "Section 10.6",
    "Section 10.7",
    "Section 10.8",
    "Section 10.9",
    "Section 10.10",
    "Mon 8:00 AM",
    "Mon 10:00 AM",
    "Mon 12:00 PM",
    "Mon 2:00 PM",
    "Mon 4:00 PM",
    "Tue 8:00 AM",
    "Tue 10:00 AM",
    "Tue 12:00 PM",
    "Tue 2:00 PM",
    "Tue 4:00 PM",
    "Wed 8:00 AM",
    "Wed 10:00 AM",
    "Wed 12:00 PM",
    "Wed 2:00 PM",
    "Wed 4:00 PM",
    "Thu 8:00 AM",
    "Thu 10:00 AM",
    "Thu 12:00 PM",
    "Thu 2:00 PM",
    "Thu 4:00 PM",
    "Fri 8:00 AM",
    "Summer 2022",
    "Fall 2022",
    "Winter 2022",
    "Spring 2022",
    "Summer 2023",
    "Fall 2023",
    "Winter 2023",
    "Spring 2023",
    "Summer 2024",
    "Fall 2024",
    "Winter 2024",
    "Spring 2024",
]

ORGANIZATION_NAMES = [
    "University of Phoenix",
    "University of California, Berkeley",
    "Brigham Young University",
    "University of Utah",
    "Cambridge University",
    "Aurora Global University",
    "Olympus Heritage Institute",
    "Veridian Scholars University",
    "Nebula Research University",
    "Arcadia Liberal Arts College",
    "MentorMind Academy",
    "EliteMinds Tutoring Services",
    "Pinnacle Prep",
    "Summit Assessment Solutions",
    "Precision Grade Expert",
    "Apporto",
    "ScholarSphere Institute",
    "AcademeLink Consortium",
    "SageBridge University",
    "Academic Edge",
    "Dallin University",
    "BYU",
]


def create_random_course(
    organization_public_uuid: str, organization_creation_timestamp: int
) -> List[Union[RegisterCoursePublicUUIDEvent, CourseEvent]]:
    register_event = RegisterCoursePublicUUIDEvent(
        lms_id=generate_random_uuid(),
        organization_public_uuid=organization_public_uuid,
    )
    course_event = CourseEvent(
        public_uuid=register_event.public_uuid,
        instructor_public_uuid=generate_random_uuid(),
        name=select_from_string_list(COURSE_NAMES),
        description=select_from_string_list(COURSE_DESCRIPTIONS),
        version_timestamp=generate_random_timestamp(organization_creation_timestamp),
    )
    return [register_event, course_event]


def create_random_section(
    organization_public_uuid: str,
    course_public_uuid: str,
    course_creation_timestamp: int,
) -> List[Union[RegisterSectionPublicUUIDEvent, SectionEvent]]:
    events = []
    register_event = RegisterSectionPublicUUIDEvent(
        lms_id=generate_random_uuid(),
        organization_public_uuid=organization_public_uuid,
    )
    section_event = SectionEvent(
        public_uuid=register_event.public_uuid,
        course_public_uuid=course_public_uuid,
        name=select_from_string_list(SECTION_NAMES),
        closed=False,
        version_timestamp=generate_random_timestamp(course_creation_timestamp),
    )
    events.extend([register_event, section_event])

    while True:
        if random.random() < 0.1:
            section_name_change_event = SectionEvent(
                public_uuid=register_event.public_uuid,
                course_public_uuid=course_public_uuid,
                name=select_from_string_list(SECTION_NAMES),
                closed=False,
                version_timestamp=generate_random_timestamp(
                    section_event.version_timestamp
                ),
            )
            events.append(section_name_change_event)
        else:
            break

    if random.random() < 0.1:
        section_closed_event = SectionEvent(
            public_uuid=register_event.public_uuid,
            course_public_uuid=course_public_uuid,
            name=section_event.name,
            closed=True,
            version_timestamp=generate_random_timestamp(
                section_event.version_timestamp
            ),
        )
        events.append(section_closed_event)

    return events


def create_random_organization() -> OrganizationEvent:
    return OrganizationEvent(
        public_uuid=generate_random_uuid(),
        name=select_from_string_list(ORGANIZATION_NAMES),
        version_timestamp=generate_random_timestamp(),
    )


if __name__ == "__main__":
    organization = create_random_organization()
    course_events = create_random_course(
        organization.public_uuid, organization.version_timestamp
    )
    section_events = create_random_section(
        organization.public_uuid,
        course_events[1].public_uuid,
        course_events[1].version_timestamp,
    )
    print([organization, *course_events, *section_events])
