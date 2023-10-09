# powergrader_event_utils

To regenerate the base python protobuf classes run this command:
```
protoc --proto_path=powergrader_utils/events/schema/ --python_out=powergrader_utils/events/proto_events/ powergrader_utils/events/schema/*.proto
```