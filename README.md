# powergrader_event_utils

To regenerate the base python protobuf classes run this command:
```
protoc --proto_path=powergrader_event_utils/events/schema/ --python_out=powergrader_event_utils/events/proto_events/ powergrader_event_utils/events/schema/*.proto
```

# Event Info
Assignments, Submissions, Grades, Embeddings, and Rubrics can not be mutated. A new one is created and then the new one gets linked to the public_id. This ensures that we maintain correct versioning for grades. IE the grade we gave was for the correct submission and assignment.

Courses, Sections, and Users can be mutated. They have a public_id (the id everything else references and something that never changes) and they have a revision id (id). The revision id helps us keep track of which version has been published to the lms and make updates without invalidating all the grading, submissions, assignments, and rubrics. Unlike the other entities, Courses, Sections and Users must be created before we can register lms info for them. There are no partial updates. If you want to update a course, you must update all the fields.

# TODO
* Add an error class, so we can get mroe information on why an event was not valid and make error handeling a lot easier. Currently all the events could throw an exception or also return False when something is not valid. It would be better if we just returned an error object describing the issue.