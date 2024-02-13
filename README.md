# powergrader_event_utils
This repo provides the protobuf definitions and python classes for the events that are used to communicate between powergrader microservices.

# Installing
For standard use, clone the repo and run
```
pip install .
```

For development use
```
pip install .[dev]
```

# Events
Assignments, Submissions, Grades, Embeddings, and Rubrics can not be mutated. A new one is created and then the new one gets linked to the public_id. This ensures that we maintain correct versioning for grades. IE the grade we gave was for the correct submission and assignment.

Courses, Sections, and Users can be mutated. They have a public_id (the id everything else references and something that never changes) and they have a revision id (id). The revision id helps us keep track of which version has been published to the lms and make updates without invalidating all the grading, submissions, assignments, and rubrics. Unlike the other entities, Courses, Sections and Users must be created before we can register lms info for them. There are no partial updates. If you want to update a course, you must update all the fields.


# Developing

## Running the tests
```
pytest tests/
```

## Updating the protobuf
`powergrader_event_utils` uses a specific version of protobuf's `protoc` to generate the python classes. This `protoc` is included in the base of the repo. To build the base protobuf classes from the `.proto` files, run the following command:

```
bash generate_protobuf.sh
```

## Formatting
For all that is good and holy, use black. The package will be installed in your environment if you installed the package with the `dev` extras. To format the code, run the following command:

```
black .
```

or even better, set up your editor to format on save.

# TODO
- Add an error class, so we can get mroe information on why an event was not valid and make error handeling a lot easier. Currently all the events could throw an exception or also return False when something is not valid. It would be better if we just returned an error object describing the issue.
- Update README.md with the new information
- Create integration tests for the events
- Make timestamps for applicable events optional
