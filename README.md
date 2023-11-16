# powergrader_event_utils

To regenerate the base python protobuf classes run this command:
```
protoc --proto_path=powergrader_event_utils/events/schema/ --python_out=powergrader_event_utils/events/proto_events/ powergrader_event_utils/events/schema/*.proto
```

# TODO
* Add an error class, so we can get mroe information on why an event was not valid and make error handeling a lot easier. Currently all the events could throw an exception or also return False when something is not valid. It would be better if we just returned an error object describing the issue.