# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: relationship.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12relationship.proto\x12\x0crelationship\"~\n\x17\x41ssignmentAddedToCourse\x12\x1e\n\x16\x61ssignment_public_uuid\x18\x01 \x01(\t\x12\x1a\n\x12\x63ourse_public_uuid\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x14\n\x0cversion_uuid\x18\x04 \x01(\t\"\x82\x01\n\x1b\x41ssignmentRemovedFromCourse\x12\x1e\n\x16\x61ssignment_public_uuid\x18\x01 \x01(\t\x12\x1a\n\x12\x63ourse_public_uuid\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x14\n\x0cversion_uuid\x18\x04 \x01(\t\"z\n\x15StudentAddedToSection\x12\x1b\n\x13student_public_uuid\x18\x01 \x01(\t\x12\x1b\n\x13section_public_uuid\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x14\n\x0cversion_uuid\x18\x04 \x01(\t\"~\n\x19StudentRemovedFromSection\x12\x1b\n\x13student_public_uuid\x18\x01 \x01(\t\x12\x1b\n\x13section_public_uuid\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x14\n\x0cversion_uuid\x18\x04 \x01(\t\"~\n\x17InstructorAddedToCourse\x12\x1e\n\x16instructor_public_uuid\x18\x01 \x01(\t\x12\x1a\n\x12\x63ourse_public_uuid\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x14\n\x0cversion_uuid\x18\x04 \x01(\t\"\x82\x01\n\x1bInstructorRemovedFromCourse\x12\x1e\n\x16instructor_public_uuid\x18\x01 \x01(\t\x12\x1a\n\x12\x63ourse_public_uuid\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x14\n\x0cversion_uuid\x18\x04 \x01(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'relationship_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ASSIGNMENTADDEDTOCOURSE']._serialized_start=36
  _globals['_ASSIGNMENTADDEDTOCOURSE']._serialized_end=162
  _globals['_ASSIGNMENTREMOVEDFROMCOURSE']._serialized_start=165
  _globals['_ASSIGNMENTREMOVEDFROMCOURSE']._serialized_end=295
  _globals['_STUDENTADDEDTOSECTION']._serialized_start=297
  _globals['_STUDENTADDEDTOSECTION']._serialized_end=419
  _globals['_STUDENTREMOVEDFROMSECTION']._serialized_start=421
  _globals['_STUDENTREMOVEDFROMSECTION']._serialized_end=547
  _globals['_INSTRUCTORADDEDTOCOURSE']._serialized_start=549
  _globals['_INSTRUCTORADDEDTOCOURSE']._serialized_end=675
  _globals['_INSTRUCTORREMOVEDFROMCOURSE']._serialized_start=678
  _globals['_INSTRUCTORREMOVEDFROMCOURSE']._serialized_end=808
# @@protoc_insertion_point(module_scope)
