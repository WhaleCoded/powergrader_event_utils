# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: relationship.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12relationship.proto\x12\x0crelationship\"E\n\x18PrivateIDAddedToPublicID\x12\x14\n\x0cprivate_uuid\x18\x01 \x01(\t\x12\x13\n\x0bpublic_uuid\x18\x02 \x01(\t\"I\n\x1cPrivateIDRemovedFromPublicID\x12\x14\n\x0cprivate_uuid\x18\x01 \x01(\t\x12\x13\n\x0bpublic_uuid\x18\x02 \x01(\t\"C\n\x17\x41ssignmentAddedToCourse\x12\x15\n\rassignment_id\x18\x01 \x01(\t\x12\x11\n\tcourse_id\x18\x02 \x01(\t\"G\n\x1b\x41ssignmentRemovedFromCourse\x12\x15\n\rassignment_id\x18\x01 \x01(\t\x12\x11\n\tcourse_id\x18\x02 \x01(\t\"?\n\x15StudentAddedToSection\x12\x12\n\nstudent_id\x18\x01 \x01(\t\x12\x12\n\nsection_id\x18\x02 \x01(\t\"C\n\x19StudentRemovedFromSection\x12\x12\n\nstudent_id\x18\x01 \x01(\t\x12\x12\n\nsection_id\x18\x02 \x01(\t\"B\n\x16InstuctorAddedToCourse\x12\x15\n\rinstructor_id\x18\x01 \x01(\t\x12\x11\n\tcourse_id\x18\x02 \x01(\t\"G\n\x1bInstructorRemovedFromCourse\x12\x15\n\rinstructor_id\x18\x01 \x01(\t\x12\x11\n\tcourse_id\x18\x02 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'relationship_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PRIVATEIDADDEDTOPUBLICID._serialized_start=36
  _PRIVATEIDADDEDTOPUBLICID._serialized_end=105
  _PRIVATEIDREMOVEDFROMPUBLICID._serialized_start=107
  _PRIVATEIDREMOVEDFROMPUBLICID._serialized_end=180
  _ASSIGNMENTADDEDTOCOURSE._serialized_start=182
  _ASSIGNMENTADDEDTOCOURSE._serialized_end=249
  _ASSIGNMENTREMOVEDFROMCOURSE._serialized_start=251
  _ASSIGNMENTREMOVEDFROMCOURSE._serialized_end=322
  _STUDENTADDEDTOSECTION._serialized_start=324
  _STUDENTADDEDTOSECTION._serialized_end=387
  _STUDENTREMOVEDFROMSECTION._serialized_start=389
  _STUDENTREMOVEDFROMSECTION._serialized_end=456
  _INSTUCTORADDEDTOCOURSE._serialized_start=458
  _INSTUCTORADDEDTOCOURSE._serialized_end=524
  _INSTRUCTORREMOVEDFROMCOURSE._serialized_start=526
  _INSTRUCTORREMOVEDFROMCOURSE._serialized_end=597
# @@protoc_insertion_point(module_scope)
